import type { RecommendationItem } from "../types/recommendation";

interface RecommendationListProps {
  recommendations: RecommendationItem[];
  totalJobsEvaluated: number;
}

function TextList({ items, emptyText }: { items: string[]; emptyText: string }) {
  if (items.length === 0) {
    return <p className="empty-detail">{emptyText}</p>;
  }

  return (
    <ul>
      {items.map((item) => <li key={item}>{item}</li>)}
    </ul>
  );
}

// Props 是父组件传入的数据。结果组件只负责展示，不负责请求 API。
export function RecommendationList({ recommendations, totalJobsEvaluated }: RecommendationListProps) {
  if (recommendations.length === 0) {
    return (
      <section className="results-panel empty-state">
        <h2>暂时没有推荐结果</h2>
        <p>可以补充更多技能或放宽岗位、地点和薪资条件后再次尝试。</p>
      </section>
    );
  }

  return (
    <section className="results-panel">
      <div className="results-heading">
        <div>
          <p className="eyebrow">第二步</p>
          <h2>你的岗位推荐</h2>
        </div>
        <p>已评估 {totalJobsEvaluated} 个岗位，为你展示前 {recommendations.length} 个结果。</p>
      </div>

      <div className="recommendation-list">
        {recommendations.map((item, index) => (
          <article className="recommendation-card" key={item.job.id}>
            <div className="card-topline">
              <span className="rank">推荐 {index + 1}</span>
              <strong className="score">{item.match_score.toFixed(1)} 分</strong>
            </div>
            <h3>{item.job.title}</h3>
            <p className="company">{item.job.company_name} · {item.job.location}</p>

            <div className="detail-grid">
              <div>
                <h4>推荐理由</h4>
                <TextList items={item.reasons} emptyText="暂无具体推荐理由。" />
              </div>
              <div>
                <h4>技能差距</h4>
                <TextList items={item.missing_skills} emptyText="暂无明显技能差距。" />
              </div>
              <div>
                <h4>下一步建议</h4>
                <TextList items={item.next_steps} emptyText="可以开始准备简历并投递。" />
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
