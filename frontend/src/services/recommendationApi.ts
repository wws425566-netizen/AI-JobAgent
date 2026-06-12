import type {
  RecommendationResponse,
  UserProfileInput,
} from "../types/recommendation";

export async function fetchRecommendations(
  profile: UserProfileInput,
): Promise<RecommendationResponse> {
  // await 表示先等待后端响应，再继续处理返回的数据。
  const response = await fetch("/api/recommendations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });

  if (!response.ok) {
    let message = "推荐请求失败，请稍后重试。";

    try {
      const errorBody = (await response.json()) as { detail?: unknown };
      if (typeof errorBody.detail === "string") {
        message = errorBody.detail;
      } else if (response.status === 422) {
        message = "提交的信息格式不正确，请检查后重试。";
      }
    } catch {
      // 后端没有返回 JSON 时，保留上面的通用中文提示。
    }

    throw new Error(message);
  }

  return (await response.json()) as RecommendationResponse;
}
