# JobAgent Backend

阶段一目标：先搭建一个最小可运行的 FastAPI + SQLite 后端。

当前阶段不使用 PostgreSQL、Alembic、Docker。

## 目录结构

```text
backend/
  app/
    api/
    core/
    models/
    schemas/
    services/
    main.py
  requirements.txt
  README.md
```

## 创建虚拟环境

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 安装依赖

```powershell
pip install -r requirements.txt
```

## 启动后端

```powershell
uvicorn app.main:app --reload
```

启动后访问：

- 健康检查：http://localhost:8000/health
- Swagger API 文档：http://localhost:8000/docs

## 当前接口

### GET /health

返回后端运行状态和 SQLite 配置信息。

### GET /api/jobs

返回 SQLite 中保存的岗位列表。

### POST /api/recommendations

接收用户画像并返回匹配分数最高的 5 个岗位。评分由必备技能、加分技能、经验、日语、岗位方向、地点和薪资组成；项目经历简介暂时只接收，不参与规则评分。

Swagger 中可以使用下面的请求数据测试：

```json
{
  "skills": ["Python", "FastAPI", "SQL", "Linux"],
  "experience_years": 1,
  "japanese_level": "N2",
  "desired_role": "backend",
  "preferred_locations": ["东京"],
  "expected_salary": 300000,
  "project_summary": "使用 FastAPI 和 SQLite 开发后端项目"
}
```

## 运行测试

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## 初始化岗位数据

```powershell
.\.venv\Scripts\python.exe -m scripts.seed_jobs
```

执行后会在 `jobagent.db` 中创建 `job_postings` 表，并写入 25 条模拟日本 IT 岗位数据。

说明：`preferred_skills` 和 `japanese_level` 允许为空，因为真实岗位信息里经常不会明确写加分技能或日语等级。

如果修改了表结构，可以用下面的命令重建本地 SQLite 数据：

```powershell
.\.venv\Scripts\python.exe -m scripts.seed_jobs --reset
```
