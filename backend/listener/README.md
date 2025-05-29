# Listing Listener

這個 service 是部署在 Render 上的背景工作者，用來持續監聽 Supabase 的 listing 資料異動事件。

## 部署步驟

1. 把此資料夾推上 GitHub（與其他程式碼同一 repo）
2. 登入 [Render](https://render.com)
3. 點選 "New → Web Service" 或 "New → Background Worker"
4. Render 會自動抓取 render.yaml 設定檔進行部署
