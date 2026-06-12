export type JapaneseLevel = "N1" | "N2" | "N3";

export type RoleCategory =
  | "backend"
  | "frontend"
  | "fullstack"
  | "infra"
  | "ai"
  | "data"
  | "qa"
  | "security"
  | "embedded"
  | "mobile"
  | "enterprise";

// 这些类型与 FastAPI 的 Pydantic Schema 一一对应，字段写错时 TypeScript 会提前提醒。
export interface UserProfileInput {
  skills: string[];
  experience_years: number;
  japanese_level?: JapaneseLevel;
  desired_role?: RoleCategory;
  preferred_locations?: string[];
  expected_salary?: number;
  project_summary?: string;
}

export interface JobPosting {
  id: number;
  title: string;
  role_category: string;
  company_name: string;
  company_type: string;
  location: string;
  industry: string;
  required_skills: string[];
  preferred_skills: string[] | null;
  japanese_level: string | null;
  experience_requirement: string;
  initial_salary: number;
  job_url: string;
  created_at: string;
}

export interface ScoreBreakdown {
  required_skills: number;
  preferred_skills: number;
  experience: number;
  japanese: number;
  role: number;
  location: number;
  salary: number;
}

export interface RecommendationItem {
  job: JobPosting;
  match_score: number;
  score_breakdown: ScoreBreakdown;
  reasons: string[];
  missing_skills: string[];
  next_steps: string[];
}

export interface RecommendationResponse {
  total_jobs_evaluated: number;
  recommendations: RecommendationItem[];
}
