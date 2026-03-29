---
name: travel-expense-tracker
description: >
  Travel expense tracking and dining log automation skill. Upload receipts, credit card
  statement screenshots, or restaurant menu photos — Claude will organize them into a
  day-by-day expense table, category totals, Dining Log restaurant records, and write
  everything to Notion or export as Excel.

  Use this skill whenever the user: uploads any receipt, bill, or statement image; mentions
  "travel expense", "receipt", "dining log", "expense tracker", "log my spending", "organize
  my receipts", "how much did I spend", "process my receipts", or any phrase combining travel
  with costs, meals, or bills. Also trigger for grocery receipts, shopping receipts, or any
  purchase records connected to a trip. Trigger aggressively — if there is a receipt image or
  any mention of trip spending, use this skill.

  中文触发词：帮我整理小票、旅行记账、账单分类、Dining Log、旅行消费汇总、把这些小票录入、
  记一下今天的花费、上传了小票/账单/收据图片。只要用户提到旅行 + 记账/整理/消费，或上传了任何收据图片，就应该使用本 skill。
---

# Travel Expense Tracker Skill

## 概览

本 skill 将旅行中产生的各类消费凭证（小票照片、信用卡截图、菜单、口头描述）自动整理为：

1. **逐日消费表** — 按日期 × 类目的明细表
2. **旅途消费汇总** — 每天总花费（含/不含住宿），加总
3. **分类总计** — 大交通、住宿、餐饮、当地交通、景点门票、购物、杂项
4. **Dining Log** — 每家餐厅的点单详情、菜品描述、人均费用
5. **校验** — 用汇率反推验算，发现不一致主动提问

输出可写入 **Notion 数据库**（如用户已连接）或导出 **Excel 文件**。

---

## Intake Gate (Inversion Pattern)

Before processing, check whether you have enough context to proceed without guessing. Ask **only** the questions that are still missing — never ask what you can already infer from the message or images.

| Missing info | Ask |
|---|---|
| No trip name or destination visible | "Which trip is this for? (e.g. Malaysia Feb 2026)" |
| Currency unclear and can't be inferred from receipts | "What currency were most expenses in?" |
| Date range unknown and receipts have no dates | "What dates did this trip cover?" |
| Notion vs Excel output preference unknown (first time user) | "Should I write this to Notion or give you an Excel file?" |

**If receipts or images are attached**, infer what you can from them first — only ask about what's genuinely ambiguous. If the destination and currency are obvious from context, skip straight to Step 1.

**DO NOT ask** about classification rules, exchange rates, or anything you can determine yourself.

---

## 输入类型识别

收到用户消息后，先判断输入类型：

| 输入类型 | 处理方式 |
|---------|---------|
| 信用卡/支付宝/微信账单截图 | → 提取每笔交易：日期、金额、币种、商家名 |
| 小票/收据照片 | → OCR 提取：商家、日期、明细、总额、币种 |
| 菜单照片 + 小票 | → 补全 Dining Log（菜名+描述+价格） |
| 口头描述（"今天吃了XXX花了RM50"） | → 直接录入，标记来源为"口述" |
| 多张图片批量上传 | → 逐张处理，合并到同一行程 |

---

## Step 1：提取消费明细

### 1.1 从图片提取

对每张上传的图片：
- 识别：商家名、日期、金额、币种
- 判断类目（见分类规则）
- 如图片模糊或金额不清晰：记录商家名 + 标注「需确认金额」，继续处理，最后统一列出疑问

### 1.2 分类规则

| 类目 | 判断依据 |
|-----|---------|
| 大交通 | 机票、火车票、长途巴士、渡轮（城市间） |
| 住宿 | 酒店、民宿、Airbnb |
| 餐饮 | 餐厅、咖啡馆、街边小吃、外卖 |
| 当地交通 | Grab、出租车、地铁、公交、摩的（城市内） |
| 景点门票 | 博物馆、景区、演出、导览 |
| 购物 | 伴手礼、超市、服装、药妆 |
| 杂项 | City tax、小费、SIM卡、洗衣、其他 |

### 1.3 汇率处理

- 默认汇率从消费日期当天推算（如无法获取，使用用户提供的或常用参考值）
- **马来西亚令吉 RM → CNY**：参考值约 1 RM ≈ 1.55 CNY（需用户确认或从账单反推）
- 所有金额统一换算为人民币（¥）展示，原币金额保留备注
- 如发现换算异常（误差 > 5%），标记并询问用户

---

## Step 2：生成逐日消费表

格式如下：

```
| 日期  | 地点         | 餐饮  | 当地交通 | 景点  | 购物  | 杂项  | 当日合计(不含住宿) |
|-------|-------------|-------|---------|-------|-------|-------|-----------------|
| 02-20 | 槟城 Day 1   | ¥XXX  | ¥XXX    | ¥XXX  | ¥XXX  | ¥XXX  | ¥XXX            |
| 02-21 | 槟城 Day 2   | ...   | ...     | ...   | ...   | ...   | ...             |
```

- 住宿单独一列或单独列表（因为住宿金额大，通常按整段旅程统计）
- 每行末尾标注当日地点（城市 + Day N）

---

## Step 3：生成分类总计

```
总计
• 大交通：¥X,XXX
• 住宿：¥X,XXX
• 餐饮：¥X,XXX
• 当地交通：¥X,XXX
• 景点门票：¥XXX
• 购物：¥XXX
• 杂项（city tax等）：¥XX
• 全程总计：¥XX,XXX
```

---

## Step 4：生成 Dining Log

对每一笔餐饮消费，生成结构化记录：

```markdown
## [餐厅名]
**Date:** YYYY-MM-DD
**同伴：** X人 / solo
**人均：** RM XX（约¥XX）
**套餐/点单：**
- [菜名]：[描述——食材、做法、口味特点]
- [菜名]：[描述]
**备注：** [就餐体验、推荐指数、再访意愿等]
```

- 如有菜单图片：从图片提取菜名和描述
- 如只有小票金额、无菜单：只记录总金额，菜名留空，标注「待补充」
- 如用户有口头补充描述：融合进 Dining Log

---

## Step 5：校验

运行以下校验：

1. **逐日合计校验**：各日消费加总 = 分类总计中除住宿和大交通外的合计
2. **汇率一致性**：如同一天有多笔 RM 消费，汇率是否一致
3. **金额完整性**：标出所有「待确认」条目，列在校验报告末尾

校验报告格式：
```
✅ 逐日合计与分类总计一致
⚠️ 以下条目需确认：
  - 02-23 某商家 金额模糊，请确认是 RM 35 还是 RM 85？
  - 02-25 住宿费用未录入，是否需要补充？
```

---

## Step 6：写入 Notion

### 固定位置
所有旅行页面统一创建在 **Travel Plans** 页面下（page_id: `32724f54-8181-80c0-a063-e312b5dafca3`）。

### 新建旅行流程
1. 用户发来行程信息 → 立刻在 Travel Plans 下创建新页面，标题格式：`[国旗emoji] [目的地] · [月份 年份]`
2. 初始页面包含行程骨架（日期、城市、待填内容占位符）
3. 用户后续发来小票/账单/菜单 → 持续完善同一页面

### 每个旅行页面的标准结构
```
🗺️ 行程概览        ← 目的地、日期、人数、总费用（完成后填入）
📊 旅途消费汇总     ← 逐日明细表（不含住宿）
💰 分类总计        ← 大交通/住宿/餐饮/交通/门票/购物/杂项
🍽️ Dining Log     ← 每家餐厅：日期、套餐、菜品描述
⚠️ 待补充          ← checklist，记录未确认的金额/信息
```

### 写入原则
- 新行程 → 新建独立页面，不复用旧页面
- 信息分批到达时 → 用 `notion-update-page` 追加，不覆盖已有内容
- 页面创建后告知用户链接

---

## 输出格式（无 Notion 时）

直接在对话中输出 Markdown 表格 + Dining Log，并提供 Excel 文件下载（调用 xlsx skill）。

Excel 结构：
- Sheet 1：逐日消费明细
- Sheet 2：分类总计
- Sheet 3：Dining Log

---

## 处理原则

- **遇到不确定，先继续处理其他条目，最后统一列出疑问**，不要每张图片都停下来问
- **模糊图片不猜测金额**，标记「待确认」
- **保留原币金额**，换算值作为参考
- **Dining Log 优先质量**：宁可菜品描述少一些，也要准确；不要捏造菜品
- **汇率反推**：如账单同时有原币和人民币，优先用实际汇率，不用参考值

---

## 常见场景示例

**场景 A：旅行结束后批量整理**
> 用户上传 20 张小票图片 + 2 张信用卡账单截图
→ 批量 OCR → 去重 → 逐日表 → 总计 → Dining Log → 写 Notion

**场景 B：每天旅途中实时记录**
> 用户每天晚上发来当天的 3-5 张小票
→ 当日消费明细 → 追加到总表 → 更新 Daily Notes

**场景 C：只有口述，没有小票**
> "今天早上喝了杯白咖啡 RM8，中午华阳冰室咖喱叻沙 RM15，晚上 Jawi House 人均 RM80"
→ 直接录入，标注来源「口述」，提醒保留小票

**场景 D：只想要 Dining Log，不要账目**
> 用户发来餐厅照片和菜单
→ 只生成 Dining Log，跳过账目步骤
