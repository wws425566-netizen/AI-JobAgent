import { useState, type FormEvent } from "react";

import type {
  JapaneseLevel,
  RoleCategory,
  UserProfileInput,
} from "../types/recommendation";

interface ProfileFormProps {
  isLoading: boolean;
  onSubmit: (profile: UserProfileInput) => Promise<void>;
}

interface FormValues {
  skills: string;
  experienceYears: string;
  japaneseLevel: "" | JapaneseLevel;
  desiredRole: "" | RoleCategory;
  preferredLocations: string;
  expectedSalary: string;
  projectSummary: string;
}

const initialValues: FormValues = {
  skills: "Python, FastAPI, SQL",
  experienceYears: "0",
  japaneseLevel: "",
  desiredRole: "backend",
  preferredLocations: "东京",
  expectedSalary: "",
  projectSummary: "",
};

const roleOptions: Array<{ value: RoleCategory; label: string }> = [
  { value: "backend", label: "后端开发" },
  { value: "frontend", label: "前端开发" },
  { value: "fullstack", label: "全栈开发" },
  { value: "infra", label: "基础设施 / 运维" },
  { value: "ai", label: "人工智能" },
  { value: "data", label: "数据开发" },
  { value: "qa", label: "软件测试" },
  { value: "security", label: "信息安全" },
  { value: "embedded", label: "嵌入式开发" },
  { value: "mobile", label: "移动端开发" },
  { value: "enterprise", label: "企业软件" },
];

function splitList(value: string): string[] {
  // 同时支持中文和英文逗号，trim 用于清除每项前后的空格。
  return value
    .split(/[,，]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export function ProfileForm({ isLoading, onSubmit }: ProfileFormProps) {
  // State 是组件中会变化的数据；setValues 更新后，React 会重新显示页面。
  const [values, setValues] = useState<FormValues>(initialValues);
  const [validationError, setValidationError] = useState("");

  function updateValue<K extends keyof FormValues>(key: K, value: FormValues[K]) {
    setValues((currentValues) => ({ ...currentValues, [key]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    // 浏览器原本会刷新页面；React 表单通常阻止刷新并自行处理数据。
    event.preventDefault();
    setValidationError("");

    const skills = splitList(values.skills);
    const experienceYears = Number(values.experienceYears);
    const expectedSalary = values.expectedSalary
      ? Number(values.expectedSalary)
      : undefined;

    if (skills.length === 0) {
      setValidationError("请至少填写一项技能。用于多项技能时，请使用逗号分隔。");
      return;
    }
    if (!Number.isInteger(experienceYears) || experienceYears < 0 || experienceYears > 50) {
      setValidationError("经验年数必须是 0 到 50 之间的整数。");
      return;
    }
    if (expectedSalary !== undefined && (!Number.isInteger(expectedSalary) || expectedSalary < 0)) {
      setValidationError("期望月薪必须是大于或等于 0 的整数。");
      return;
    }

    const locations = splitList(values.preferredLocations);
    const projectSummary = values.projectSummary.trim();

    await onSubmit({
      skills,
      experience_years: experienceYears,
      ...(values.japaneseLevel && { japanese_level: values.japaneseLevel }),
      ...(values.desiredRole && { desired_role: values.desiredRole }),
      ...(locations.length > 0 && { preferred_locations: locations }),
      ...(expectedSalary !== undefined && { expected_salary: expectedSalary }),
      ...(projectSummary && { project_summary: projectSummary }),
    });
  }

  return (
    <form className="profile-form" onSubmit={handleSubmit}>
      <div className="form-heading">
        <p className="eyebrow">第一步</p>
        <h2>填写你的求职画像</h2>
        <p>带 * 的字段必须填写，其余信息填写得越完整，推荐越贴近你的期望。</p>
      </div>

      <div className="form-grid">
        <label className="field field-wide">
          <span>掌握的技能 *</span>
          <input
            value={values.skills}
            onChange={(event) => updateValue("skills", event.target.value)}
            placeholder="例如：Python, FastAPI, SQL"
          />
          <small>多项技能请使用中文或英文逗号分隔。</small>
        </label>

        <label className="field">
          <span>工作或实习经验（年）*</span>
          <input
            type="number"
            min="0"
            max="50"
            step="1"
            value={values.experienceYears}
            onChange={(event) => updateValue("experienceYears", event.target.value)}
          />
        </label>

        <label className="field">
          <span>日语等级</span>
          <select
            value={values.japaneseLevel}
            onChange={(event) => updateValue("japaneseLevel", event.target.value as FormValues["japaneseLevel"])}
          >
            <option value="">暂未选择</option>
            <option value="N1">N1</option>
            <option value="N2">N2</option>
            <option value="N3">N3</option>
          </select>
        </label>

        <label className="field">
          <span>期望岗位方向</span>
          <select
            value={values.desiredRole}
            onChange={(event) => updateValue("desiredRole", event.target.value as FormValues["desiredRole"])}
          >
            <option value="">不限方向</option>
            {roleOptions.map((option) => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>期望工作地点</span>
          <input
            value={values.preferredLocations}
            onChange={(event) => updateValue("preferredLocations", event.target.value)}
            placeholder="例如：东京, 大阪"
          />
        </label>

        <label className="field">
          <span>期望月薪（日元）</span>
          <input
            type="number"
            min="0"
            step="10000"
            value={values.expectedSalary}
            onChange={(event) => updateValue("expectedSalary", event.target.value)}
            placeholder="例如：300000"
          />
        </label>

        <label className="field field-wide">
          <span>项目经历简介</span>
          <textarea
            rows={4}
            maxLength={2000}
            value={values.projectSummary}
            onChange={(event) => updateValue("projectSummary", event.target.value)}
            placeholder="简单介绍你做过的项目、使用的技术和负责的内容。"
          />
          <small>{values.projectSummary.length}/2000 字</small>
        </label>
      </div>

      {validationError && <p className="message error-message">{validationError}</p>}

      <button className="submit-button" type="submit" disabled={isLoading}>
        {isLoading ? "正在分析岗位..." : "获取岗位推荐"}
      </button>
    </form>
  );
}
