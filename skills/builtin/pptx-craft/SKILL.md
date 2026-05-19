---
name: pptx-craft
description: "PPT 生成技能。用户说「生成PPT」「华为风格PPT」「做成PPT」时触发。直接执行生成流程，不创建子agent。"
---

# PPT 生成技能

## Absolute Priority Rules

When the user asks to generate/create a PPT presentation, obey these rules in order:

1. **If user says "生成PPT" / "做成PPT" / "华为风格PPT"**:
   **MUST EXECUTE:** `node /Users/yiyu/Pyleaf/ollama-mlflow-demo/skills/builtin/pptx-craft/scripts/utils/generate_timestamp_dir.js output/`
   Then use Write tool to create outline.md in the output directory.

2. **Prohibited:** Do NOT create sub-agents. Do NOT use Agent tool.

3. **Direct execution:** Generate HTML slides yourself, then call convert.js to export PPTX.

---

## Step-by-step Workflow

### Step 1: Create Output Directory

**Exact command:**
```bash
node /Users/yiyu/Pyleaf/ollama-mlflow-demo/skills/builtin/pptx-craft/scripts/utils/generate_timestamp_dir.js output/
```

Script returns path like: `output/20260519_120000_000/`

### Step 2: Write Outline

Use Write tool to create `{output_dir}/outline.md`.

### Step 3: Create pages Directory

```bash
mkdir -p {output_dir}/pages
```

### Step 4: Generate HTML Slides

**CRITICAL: Use Tailwind CSS CDN and `.ppt-slide` class!**

**封面页 Template (华为风格):**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1280, height=720">
  <title>封面 - {主题}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap');
    * { font-family: 'Noto Sans SC', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
    body { width: 1280px; height: 720px; overflow: hidden; }
  </style>
</head>
<body class="w-[1280px] h-[720px] overflow-hidden">
  <div class="ppt-slide" style="width:1280px;height:720px;position:relative;overflow:hidden;background:#c7020e;">
    <!-- 装饰纹理 -->
    <div style="position:absolute;top:0;right:0;width:500px;height:500px;opacity:0.06;">
      <div style="position:absolute;top:50px;right:50px;font-size:300px;font-weight:900;color:white;line-height:1;">AI</div>
    </div>
    <!-- 装饰线条 -->
    <div style="position:absolute;top:120px;left:80px;width:200px;height:4px;background:rgba(255,255,255,0.6);"></div>
    <!-- 主标题 -->
    <div style="position:absolute;top:220px;left:80px;">
      <div style="font-size:18px;color:rgba(255,255,255,0.8);font-weight:300;letter-spacing:8px;margin-bottom:16px;">PRESENTATION</div>
      <h1 style="font-size:62px;font-weight:900;color:white;line-height:1.2;letter-spacing:4px;">{标题}</h1>
      <div style="margin-top:24px;font-size:24px;color:rgba(255,255,255,0.7);font-weight:300;">{副标题}</div>
    </div>
    <!-- 底部 -->
    <div style="position:absolute;bottom:60px;left:80px;font-size:16px;color:rgba(255,255,255,0.5);">{底部文字}</div>
    <div style="position:absolute;bottom:60px;right:80px;font-size:16px;color:rgba(255,255,255,0.5);">01</div>
  </div>
</body>
</html>
```

**内页 Template (华为风格):**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1280, height=720">
  <title>{标题}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap');
    * { font-family: 'Noto Sans SC', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
    body { width: 1280px; height: 720px; overflow: hidden; }
  </style>
</head>
<body class="w-[1280px] h-[720px] overflow-hidden bg-white">
  <div class="ppt-slide" style="width:1280px;height:720px;position:relative;overflow:hidden;background:white;">
    <!-- 顶部装饰线 -->
    <div class="w-full h-[1px] bg-[#c7020e]"></div>
    <!-- 标题栏 -->
    <div class="w-full h-[90px] bg-white border-b border-[#d9d9d9] flex items-center px-8 gap-3">
      <div class="w-[4px] h-[30px] bg-[#c7020e]"></div>
      <span class="text-[35px] font-bold text-black">{标题}</span>
      <span class="text-[19px] text-[#8c8c8c] ml-1">{英文副标题}</span>
      <span class="ml-auto text-[19px] text-[#8c8c8c]">{页码}</span>
    </div>
    <!-- 内容区 -->
    <div class="w-full h-[calc(720px-90px-1px)] bg-white flex flex-col p-8 gap-6">
      {内容}
    </div>
  </div>
</body>
</html>
```

**华为风格关键规范:**

| 元素 | Tailwind 类名 |
|------|--------------|
| 华为红 | `bg-[#c7020e]` `text-[#c7020e]` `border-[#c7020e]` |
| 华为灰 | `text-[#8c8c8c]` `border-[#d9d9d9]` `bg-[#f2f2f2]` |
| 红色背景卡片 | `bg-[#fff1ef] border-[#c7020e]` |
| 标题字号 | `text-[35px] font-bold` |
| 正文字号 | `text-[19px]` |
| 辅助字号 | `text-[16px] text-[#8c8c8c]` |
| 标题栏高度 | `h-[90px]` |
| 红色指示条 | `w-[4px] h-[30px] bg-[#c7020e]` |

**File naming:** `page-1.pptx.html`, `page-2.pptx.html`, etc. (with hyphen!)

### Step 5: Export PPTX

**Exact command:**
```bash
node /Users/yiyu/Pyleaf/ollama-mlflow-demo/skills/builtin/pptx-craft/html-to-pptx/scripts/convert.js {output_dir}/pages/ {output_dir}/{主题}.pptx
```

**⚠️ Bash timeout 设置：**
- 转换需要约 10秒/页
- 推荐 timeout=600（使用默认值即可，不传递timeout参数）
- 如有大量页面（>50页），可设置 timeout=1200 或更大（max: 3600）

### Step 6: Deliver

Verify PPTX file exists and is > 10KB. Tell user the file path.

---

## Gotchas

- **CRITICAL: Use `.ppt-slide` class** — The container MUST have `class="ppt-slide"`
- **CRITICAL: Use Tailwind CSS CDN** — `<script src="https://cdn.tailwindcss.com"></script>`
- **CRITICAL: Bash timeout** — 使用默认600秒，大量页面可设置 timeout=1200 或更大（max: 3600）
- **Use Tailwind 任意值语法** — `text-[35px]`, `text-[#c7020e]`, `w-[4px]`
- **File naming:** page-1.pptx.html (with hyphen)
- **Page size:** 1280x720px fixed
- **No sub-agents:** Execute all steps directly

---

## Debugging Conversion Issues

If convert.js fails or produces unexpected output:

- **Do NOT read convert.js** — It's a 400KB obfuscated JavaScript bundle, unreadable by humans/LLMs
- **Do NOT use Read tool on convert.js** — Large file may cause API errors or model confusion
- **Correct approach:** Run convert.js and check the actual error output:
  ```bash
  node /path/to/convert.js pages_dir/ output.pptx 2>&1
  ```
- **Common errors:**
  - `未找到 .ppt-slide 元素` → HTML missing the `.ppt-slide` class
  - `paths[0] undefined` → Missing or invalid input/output arguments
  - `[Error] Command timed out after Xs` → Bash timeout too short, use default 600 or increase
- **Check generated HTML files first** — Verify `.ppt-slide` class exists before debugging conversion