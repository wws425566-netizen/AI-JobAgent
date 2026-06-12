# JobAgent 前端

这是 JobAgent 的 React 网页。用户填写求职画像后，页面调用 FastAPI 推荐接口并展示岗位结果。

## 先理解几个文件

- `package.json`：记录项目命令和第三方依赖，类似 Python 项目的 `requirements.txt`。
- `index.html`：浏览器最先打开的 HTML，其中的 `root` 节点用于挂载 React。
- `src/main.tsx`：JavaScript 入口，负责把根组件放进 HTML。
- `src/App.tsx`：根组件，管理请求结果、loading 和错误等共享状态。
- `src/components/`：页面组件。组件就是可以独立维护、重复组合的界面部分。
- `src/services/`：集中管理后端 API 请求，避免请求代码散落在组件里。
- `src/types/`：TypeScript 数据类型，用来约束前后端字段。
- `src/styles.css`：CSS 样式，负责布局、颜色、间距和移动端适配。
- `vite.config.ts`：Vite 配置。开发代理会把 `/api` 转发到后端的 `8000` 端口。

## 前端基础概念

- **组件 Component**：用函数描述一块界面，例如表单和推荐列表。
- **Props**：父组件传给子组件的数据或函数，子组件不能随意修改它。
- **State**：组件内部会变化的数据。调用 `setState` 后，React 自动更新界面。
- **事件处理**：`onChange` 响应输入，`onSubmit` 响应表单提交。
- **异步请求**：`fetch` 请求后端需要时间，使用 `async/await` 等待结果。
- **TypeScript 类型**：在运行前检查字段名和数据类型，减少前后端联调错误。
- **CSS**：只改变页面外观，不负责推荐业务逻辑。

## 本地启动

先打开一个 PowerShell，启动后端：

```powershell
cd D:\Codex\JobAgent\backend
.\.venv\Scripts\Activate.ps1
python -m scripts.seed_jobs
uvicorn app.main:app --reload
```

再打开另一个 PowerShell，启动前端：

```powershell
cd D:\Codex\JobAgent\frontend
npm.cmd install
npm.cmd run dev
```

PowerShell 禁止运行 `npm.ps1` 时，使用 `npm.cmd` 即可。浏览器访问终端显示的地址，默认是 `http://localhost:5173`。

## 常用命令

```powershell
# 启动开发服务器，修改代码后页面会自动刷新
npm.cmd run dev

# 检查 TypeScript 类型
npm.cmd run typecheck

# 创建可部署的生产版本，输出到 dist/
npm.cmd run build
```

## 一次提交发生了什么

1. `ProfileForm` 使用 State 保存输入框内容。
2. 用户提交时，表单检查技能、经验和薪资是否合法。
3. 文本形式的技能和地点被转换成字符串数组。
4. `App` 显示 loading，并调用 `fetchRecommendations`。
5. Vite 把 `/api/recommendations` 请求转发给 FastAPI。
6. 请求成功后，`RecommendationList` 通过 Props 接收结果并展示卡片。
7. 请求失败时，页面结束 loading 并显示中文错误信息。
