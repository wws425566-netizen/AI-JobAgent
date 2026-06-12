import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from "./App";

// main.tsx 是前端入口：找到 index.html 的 root 节点，再把 App 组件放进去。
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
