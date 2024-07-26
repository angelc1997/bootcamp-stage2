# [台北一日遊](http://100.28.23.193:8000/)


# 目錄

- [功能說明](#功能說明)
- [技術架構](#技術架構)
- [專案說明](#專案說明)

# 功能說明

- 提供使用搜尋框或是卷軸地名選單進行地點查詢
- 提供會員預約景點導覽
- 串接Tappay，支援信用卡付款預約行程

# 技術架構

- 前端框架：HTML、CSS、Javascript
- 後端串接：Python FastAPI
- 資料庫：MySQL
- 部署：AWS EC2
- 版本控制：GitHub
- 其他套件：Python參照 [requirements.txt](https://github.com/angelc1997/bootcamp-stage2/blob/refactor/requirements.txt) 套件下載

# 專案說明

[版本一](https://github.com/angelc1997/bootcamp-stage2/tree/develop)：未加入前後端分離以及MVC架構

[版本二](https://github.com/angelc1997/bootcamp-stage2/tree/refactor)：以下說明

### 前端

- 將Javascript依照不同功能分成多檔案，以提升維護
- 導入SCSS，自訂變數，以模組方式區分頁面以及元件渲染風格
- 使用gulp自動編譯SCSS為可讀CSS

### 後端
- 導入MVC架構，區分資料數據與路由執行檔

### 部署
- 以systemd檔案自動啟用、停止服務

