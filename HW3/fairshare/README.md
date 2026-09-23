# FairShare 室友分帳神器 (College Roommate Expense & Utility Manager)

國立金門大學 資訊工程學系 軟體工程專題作業  
習題 3：請想出一個有價值的專案程式，並實作出來

---

## 0. 專案價值問答評估 (Project Value Q&A)

### Q1：使用價值（Utility Value）

- **自己就是核心使用者？**
  - **是。** 作為校外合租透天與公寓的大學生，我與室友（多達 8 至 10 人規模、跨樓層居住）每逢雙月皆需面對台電總帳單的分拆困擾。各房冷氣分電表指針不一、公共冰箱與走廊用電無人認領、單人房與雙人同住房型分攤基準不對等，且日常日用品採買（垃圾袋、衛生紙、濾芯）代墊款項雜亂。本專案正是為了解決自身日常生活中的真實痛點而生。
- **你知道很多人想要這個？**
  - **是。** 大專院校周邊有龐大的大學生外宿族群，多數合租群體目前僅能依賴 LINE 記事本手動記錄或使用通用的分帳軟體。然而現有市售工具（如 Splitwise）無法動態處理台灣特有的「台電階梯累進費率＋獨立分電表加權＋公電均攤」複雜算式，亦無法靈活調整「一房多人住」的加權人數。此類需求在大學生租屋社團與 Dcard 居家生活版/心情版常年引發高度討論，具備廣大且精準的受眾需求。

### Q2：商業價值（Commercial Value）

- **已知商業模式（Proven Business Models）：**
  - **Freemium 訂閱制（進階功能加值）：** 基礎分表計算與記帳功能完全免費開放，高階功能（如帳單 OCR 自動辨識、PDF/Excel 租屋收支明細一鍵匯出、LINE Notify 自動推播欠費提醒與催繳通知）採小額月租訂閱模式。
- **新商業模式（New Business Opportunities）：**
  - **房東/物業代管 SaaS 輕量化系統：** 許多包租代管業者與多套房房東缺乏現代化管理工具，FairShare 可延伸為「房東端批次管理後台」，提供批次匯入台電帳單、自動生成各房繳費單與 LINE Pay / 台灣 Pay 繳費 QR Code，向房東收取年費或單筆出單手續費。
  - **在地生活圈精準推播與特約導購：** 掌握大學生合租生活型態後，可與周邊學生生活服務合作，於介面中整合大型賣場日用品箱購優惠、搬家服務、水電修繕媒合抽成。
- **接案與技術變現潛力（Freelance & Contracting）：**
  - 本專案完整涵蓋前端響應式狀態流、後端演算法設計（債務最小化沖抵模型、非線性加權拆算）與關聯式資料庫架構，具備高度模組化特性。可作為向校外包租代管公司、大專院校周邊學生公寓物業展示之接案作品集（Portfolio），直接承接學生宿舍管理系統、物業水電自動結算儀表板等客製化軟體外包專案。

---

## 1. 作者與學生資訊 (Author Information)

- **學校單位：** 國立金門大學 資訊工程學系 (National Quemoy University, Department of Computer Science and Information Engineering)
- **年級班別：** 資訊工程學系四年級
- **學號：** 111210557
- **姓名：** 范權榮 (Fan, Quan-Rong)

---

## 2. 專案背景與痛點分析 (Problem Statement & Value Proposition)

在大學外宿生態中，多人（特別是 3 至 10 人規模）共同承租整層公寓或多樓層透天厝是非常普遍的居住型態。然而，缺乏系統化管理機制的合租生活，往往在每月底結算各項生活開銷時面臨繁瑣的人工作業，甚至演變成室友間的人際矛盾與誠信摩擦。本專案鎖定以下核心痛點進行工程化解決：

### 2.1 台電累進費率與獨立電表拆算失衡

台灣電力公司的住宅用電計費採用「階梯累進費率」制（度數愈高，每度邊際單價愈昂貴）。租屋處各房雖常加裝獨立分電表以記錄各房冷氣用電，但公共區域設備（如公共冰箱、走廊感應燈、加壓馬達、客廳冷氣、電熱水器）所消耗的公電度數無法直接歸屬給單一房間。若房東僅提供一張台電總帳單，室友之間手動計算每度平均單價並拆解「私人冷氣用電」與「全室公電均分額」極易產生計算錯誤與公平性爭議。

### 2.2 房間坪數差異與雙人合住情境

租屋空間中各房型的配置條件並不對等，例如套房自帶衛浴、雅房面積較小、某些房間甚至具備突出窗外掛衣空間。此外，部分房間由單人居住，部分大房間則由兩位室友共同分擔。若採取無差別的死板「人頭均分制」分攤租金與公電，容易引發小坪數住戶的不滿。系統必須具備動態調整各房入住人數與獨立設定權重的彈性。

### 2.3 日常消耗品代墊款項混亂與繁瑣轉帳

日常合租生活伴隨大量的瑣碎雜支代墊，例如專用垃圾袋、洗碗精、好市多衛生紙、公共濾水器濾芯替換等。過往室友通常透過通訊軟體記事本草草記帳，日積月累後不僅容易漏帳，月底結算時更需要多位室友彼此間互相轉帳數十元零錢。本系統導入債務最小化沖抵模型，將複雜的多邊交易鏈濃縮為最精簡的淨額清償路徑。

### 2.4 公共修繕通報缺乏進度看板

當租屋處設備發生故障（如一樓浴室蓮蓬頭軟管過短漏水、走廊燈具毀損、冷氣機故障等），往往存在通報責任分散的現象，容易出現「甲以為乙已聯絡房東，實際上無人處理」的溝通斷層。透明化的修繕狀態看板能確保所有住戶隨時掌握報修進度與負責人。

---

## 3. 系統核心架構與功能模組 (System Architecture & Modules)

本專案採用現代化全端架構分離設計，包含三大業務功能模組：

### 3.1 水電獨立分表動態拆算模組 (Utility & Sub-meter Module)

- **動態房間拓撲配置：** 允許使用者自由新增、命名、修改與刪除房間節點，完全解除傳統寫死房間陣列的限制，能靈活適配不同承租戶型。
- **人數與指針參數綁定：** 支援即時輸入各房本期與上期的電表指針讀數，並支援設定該房的實際入住人數（例如單人雅房或雙人套房）。
- **雙重費用透明輸出：** 自動展示全室用電之平均度數單價、公電總度數，並清楚列出各房間之「總應付金額」與「每人應付分攤額」。

### 3.2 共同雜支記帳與代墊管理模組 (Shared Expense Ledger)

- **即時交易表記錄：** 提供互動式彈窗表單，允許住戶快速登錄品項名稱、代墊室友、消費金額與記錄日期。
- **響應式資料表格：** 支出資訊即時同步至前端資料表，提供代墊人身分標籤識別，確保帳目清晰公開。

### 3.3 租屋公共修繕看板模組 (Maintenance Issue Board)

- **故障狀態生命週期追蹤：** 支援登錄故障細節與通報者姓名，並標記處理階段（例如「待處理」、「已報修房東」、「已修復」）。
- **視覺化卡片呈現：** 藉由不同層級的語意化狀態標籤，即時揭露修繕進程，消除資訊不對稱。

---

## 4. 核心演算法數學模型 (Mathematical Formulations)

### 4.1 階梯式電價加權與公電均攤模型

設台電官方帳單總金額為 $B$ (新台幣)，台電官方總用電度數為 $K_{\text{total}}$ (度)。  
系統內共有 $N$ 間房，第 $i$ 間房的指針差值為 $U_i$：

$$U_i = \max(0, \text{currKwh}_i - \text{prevKwh}_i)$$

1. **台電平均每度加權單價 ($R$)：**
   $$R = \frac{B}{K_{\text{total}}}$$

2. **私人房間用電度數總和 ($K_{\text{private}}$)：**
   $$K_{\text{private}} = \sum_{i=1}^{N} U_i$$

3. **公共區域用電度數 ($K_{\text{common}}$)：**
   $$K_{\text{common}} = \max(0, K_{\text{total}} - K_{\text{private}})$$

4. **全室總入住人數 ($P_{\text{total}}$)：**
   設第 $i$ 間房的入住人數為 $p_i$，則：
   $$P_{\text{total}} = \sum_{i=1}^{N} p_i$$

5. **每人應負擔之公共用電費用 ($C_{\text{common\_per\_person}}$)：**
   $$C_{\text{common\_per\_person}} = \frac{K_{\text{common}} \times R}{P_{\text{total}}}$$

6. **房間 $i$ 之本期水電結算總額 ($\text{Total}_i$)：**
   $$\text{Total}_i = \text{round}(U_i \times R + C_{\text{common\_per\_person}} \times p_i)$$

7. **房間 $i$ 內每位室友之實付金額 ($\text{PerHead}_i$)：**
   $$\text{PerHead}_i = \text{round}\left(\frac{\text{Total}_i}{p_i}\right)$$

### 4.2 多方債務最小化沖抵演算法 (Debt Simplification)

後端演算法將多筆代墊款項轉化為有向加權圖，計算每位使用者的淨餘額（Net Balance = 總支付款項 - 應攤款項）：

- 淨餘額為正者歸入**債權人集合 (Creditors)**，代表代墊金額大於消費額。
- 淨餘額為負者歸入**債務人集合 (Debtors)**，代表享受服務但尚未完全支付。

透過雙指針貪婪配對演算法，每次取最大債務人與最大債權人進行沖抵，輸出最少筆數的轉帳交易清單，完全杜絕 $O(V^2)$ 的多方循環轉帳現象。

---

## 5. 技術選型與技術棧 (Tech Stack Specifications)

- **前端框架 (Frontend Framework)：** React 18 搭配 TypeScript，提供嚴格的型別安全與穩定的組件化架構。
- **建置工具 (Build Tool)：** Vite，具備秒級熱模組重載 (Hot Module Replacement, HMR) 與優異的生產環境打包效能。
- **樣式解決方案 (Styling Solution)：** Tailwind CSS，採用 Utility-First 概念實現現代、清爽且易維護的介面。
- **圖標庫 (Iconography)：** Lucide React，提供一致且輕量化的 SVG 圖標組件。
- **後端伺服器 (Backend Runtime)：** Node.js 搭配 Express 框架與 TypeScript，實現 RESTful API 規範。
- **資料庫與 ORM (Database & ORM)：** SQLite 嵌入式資料庫配合 Prisma ORM，本機開箱即用免配置獨立資料庫伺服器，同時具備平滑遷移至 PostgreSQL 的能力。

---

## 6. 專案目錄結構 (Project Directory Layout)

```text
fairshare/
├── README.md                          # 專案完整工程規格與說明文件
├── backend/                           # 後端 Express + Prisma 服務
│   ├── prisma/
│   │   └── schema.prisma              # 關聯式資料庫綱要與資料表定義
│   ├── src/
│   │   ├── utils/
│   │   │   ├── debtSimplifier.ts      # 貪婪式債務沖抵最小化演算法
│   │   │   └── utilityCalculator.ts   # 電表分攤與加權租金運算核心
│   │   └── server.ts                  # Express API 伺服器啟動入口
│   ├── package.json                   # 後端依賴配置
│   └── tsconfig.json                  # 後端 TypeScript 編譯配置
└── frontend/                          # 前端 React + Vite + Tailwind 應用
    ├── src/
    │   ├── App.tsx                    # 核心互動儀表板 (水電拆算/記帳/修繕)
    │   ├── index.css                  # Tailwind 指令與全域樣式定義
    │   └── main.tsx                   # React DOM 應用掛載點
    ├── tailwind.config.js             # Tailwind CSS 內容掃描配置
    ├── vite.config.ts                 # Vite 建置配置
    └── package.json                   # 前端依賴配置
```

---

## 7. 安裝與執行部署指南 (Installation & Deployment)

### 7.1 前置環境需求

- Node.js 版本建議：v18.0.0 或更高版本
- npm 版本建議：v9.0.0 或更高版本

### 7.2 後端伺服器啟動

開啟終端機視窗執行以下指令：

```bash
cd fairshare/backend
npm install
npm run dev
```

- 後端服務預設運行於：`http://localhost:5000`
- 服務狀態健康檢查端點：`http://localhost:5000/api/health`

### 7.3 前端應用啟動

開啟第二個獨立的終端機視窗執行以下指令：

```bash
cd fairshare/frontend
npm install
npm run dev
```

- 前端開發伺服器預設運行於：`http://localhost:5173`
- 啟動後在瀏覽器訪問該網址，即可直接操作包含動態房間增減、台電帳單即時試算、代墊記帳及修繕看板之完整功能。

---

## 8. RESTful API 端點規範 (API Specification)

| HTTP 方法 | 路徑                   | 功能說明           | 備註                                             |
| :-------- | :--------------------- | :----------------- | :----------------------------------------------- |
| `GET`     | `/api/health`          | 伺服器健康狀態檢查 | 回傳後端運作狀態字串                             |
| `POST`    | `/api/rent/split`      | 加權房租試算端點   | 接收總租金與各房坪數、人數陣列，回傳各房應付金額 |
| `POST`    | `/api/expenses/settle` | 債務最小化結算端點 | 接收室友淨額陣列，回傳簡化後的最少筆數轉帳指示   |

---

## 9. 軟體工程價值與總結 (Engineering Value)

本專案結合軟體工程核心原則：

1. **高內聚低耦合：** 將計費邏輯與介面展示完全解耦，核心拆算與沖抵邏輯封裝於純函數 (Pure Functions) 中，便於未來導入 Jest 單元測試。
2. **防禦性程式設計：** 包含預設數值處理、負數度數防護、零值防除錯保護，確保不同房型組合下的運算健全性。
3. **高實用性與可維護性：** 針對大學生租屋現實情境痛點進行精準設計，有效解決生活帳目痛點，具備清晰的商業應用價值與擴展性。

---

## 10. AI 協同開發與智慧代理架構 (AI Agents & Tooling)

本專案於需求工程、演算法實作、介面建構與測試部署過程中，深度採用了多代理人架構（Multi-Agent System）與現代 AI 開發工具鏈協同完成：

### 10.1 核心 AI 工具鏈 (Integrated AI Tooling)

- **OpenCode + Big Pickle Pipeline：** 用於後端關聯式資料模型設計與代碼重構，自動分析 Prisma ORM 綱要並提供防禦性例外處理建議。
- **Muse Spark 1.3：** 負責前端 Tailwind CSS 與響應式元件版面調優，輔助產出多欄位表單與彈窗互動狀態流。
- **Nexus ReAct Agent Engine：** 負責自動化執行指令、單元測試路徑推導與程式碼語意健檢。

### 10.2 專案內部代理人編制 (Agent Roles Specification)

- **Architecture & Database Agent：** 負責資料模型設計、正規化校驗與 RESTful API 端點介面規範制定。
- **Algorithmic Math Agent：** 負責台電累進電價加權演算法、非線性度數拆解與貪婪最小交易次數（Debt Simplification）演算法之數學建模與邊界案例測試。
- **UI/UX & Accessibility Agent：** 負責監控前端狀態管理（React Hooks）、輸入驗證反饋與無障礙網頁體驗優化。
- **QA & Code Review Agent：** 自動比對 Pull Request 差異，執行靜態型別檢查（TypeScript Strict Mode）與潛在內存洩漏掃描。

---

## 11. 授權條款 (License)

本專案基於 [MIT License](LICENSE) 授權開源發布。
