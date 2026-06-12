import { useState } from "react";

import { ProfileForm } from "./components/ProfileForm";
import { RecommendationList } from "./components/RecommendationList";
import { fetchRecommendations } from "./services/recommendationApi";
import type { RecommendationResponse, UserProfileInput } from "./types/recommendation";
import "./styles.css";

function App() {
  // App 保存整个页面共享的请求状态，再通过 Props 交给子组件使用。
  const [result, setResult] = useState<RecommendationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleProfileSubmit(profile: UserProfileInput) {
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetchRecommendations(profile);
      setResult(response);
    } catch (requestError) {
      // fetch 在断网或后端未启动时通常抛出 TypeError，这里统一转换成易懂的中文。
      const message = requestError instanceof TypeError
        ? "无法连接推荐服务，请确认后端已经启动。"
        : requestError instanceof Error
          ? requestError.message
          : "推荐请求失败，请稍后重试。";
      setError(message);
    } finally {
      // 无论成功还是失败都要结束 loading，否则按钮会一直处于禁用状态。
      setIsLoading(false);
    }
  }

  return (
    <main>
      <header className="hero">
        <div className="hero-content">
          <p className="brand">JOBAGENT</p>
          <h1>找到更适合你的第一份技术工作</h1>
          <p>填写你的技能与求职期望，系统会根据岗位要求给出匹配分数、技能差距和行动建议。</p>
        </div>
      </header>

      <div className="page-content">
        <ProfileForm isLoading={isLoading} onSubmit={handleProfileSubmit} />

        {isLoading && (
          <section className="message loading-message" aria-live="polite">
            正在对比岗位要求，请稍候...
          </section>
        )}
        {error && <section className="message error-message">{error}</section>}
        {result && !isLoading && (
          <RecommendationList
            recommendations={result.recommendations}
            totalJobsEvaluated={result.total_jobs_evaluated}
          />
        )}
      </div>
    </main>
  );
}

export default App;
