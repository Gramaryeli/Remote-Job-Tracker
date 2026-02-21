# 🚀 Remote Job Auto Scraper (远程工作自动筛选器)

这是一个基于 Python 和 GitHub Actions 构建的轻量级、全自动远程工作追踪工具。它能够每天定时从指定的招聘网站（如 WeWorkRemotely、Dribbble 等）拉取最新的职位信息，根据自定义的技能关键词进行智能筛选，并将匹配的优质职位导出为 CSV 表格。

## ✨ 核心功能 (Features)
- **☁️ 云端全自动运行**：利用 GitHub Actions 每天北京时间早上 8:00 准时触发，无需本地开机。
- **🎯 极其精准的过滤**：通过 `feedparser` 解析 RSS 源，精准提取标题或描述中包含 `Python`, `Scraping`, `Automation`, `Data Analysis` 等关键词的职位。
- **🛡️ 稳定与兼容**：自带时区处理 (`UTC+8`)，内置伪装请求头，轻量、快速且不惧怕常见的反爬策略。
- **📧 邮件自动推送**：运行结束后，将生成的 CSV 表格直接作为附件发送到私人邮箱（配置中）。

## 🛠️ 技术栈 (Tech Stack)
- **Python 3.10** (`requests`, `feedparser`, `csv`)
- **CI/CD**: GitHub Actions workflows

## ⚙️ 如何使用 (Usage)
1. Fork 本仓库。
2. 修改 `job_filter.py` 中的 `MY_KEYWORDS` 为你自己的专属技能关键词。
3. （可选）在 `rss_urls` 中添加更多支持 RSS 的招聘网站源。
4. 开启仓库的 Actions 权限，它将在明天早上为你推送第一份工作清单！

---
*Created by [Gramaryeli] - 探索自动化与数据提取的无限可能。*
