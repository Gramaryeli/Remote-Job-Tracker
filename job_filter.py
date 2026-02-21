import requests
import feedparser
import csv
from datetime import datetime

# 移除了本地代理环境专用的 urllib3 证书忽略代码

rss_urls = [
    "https://weworkremotely.com/categories/remote-data-jobs.rss",  # WWR 的数据类工作专属通道
    "https://weworkremotely.com/categories/remote-programming-jobs.rss",  # WWR 的所有编程类工作
]

MY_KEYWORDS = [
    "python",
    "scraping",
    "web scraping",
    "crawler",  # 爬虫抓取类
    "data extraction",
    "data analysis",
    "data processing",  # 数据提取与处理类
    "automation",
    "script",
    "bot",  # 自动化与脚本类
    "tool",
    "utility",  # 实用工具类
]


def fetch_and_filter_jobs():
    matched_jobs = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    }

    # [核心修改点] 移除了本地 Clash Verge 的 7897 代理配置
    # 因为 GitHub Actions 的服务器在海外，可以直接流畅访问这些网站

    print("🔍 开始从 RSS 源拉取并分析最新职位...\n")
    print("-" * 50)

    for url in rss_urls:
        try:
            # [核心修改点] 移除了 proxies 和 verify=False 参数，回归最干净的请求方式
            response = requests.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                print(f"❌ 被拦截或失效: {url} (HTTP 状态码: {response.status_code})")
                continue

            feed = feedparser.parse(response.content)
            total_entries = len(feed.entries)
            print(f"✅ 成功连接: {url}")
            print(f"   -> 获取到 {total_entries} 条原始职位数据")

            match_count_for_this_site = 0
            for entry in feed.entries:
                title = entry.title.lower()
                summary = entry.get("summary", "").lower()

                if any(
                    keyword in title or keyword in summary for keyword in MY_KEYWORDS
                ):
                    match_count_for_this_site += 1
                    matched_jobs.append(
                        {
                            "职位名称": entry.title,
                            "发布时间": entry.get("published", "未知时间"),
                            "职位链接": entry.link,
                            "数据来源": url,
                        }
                    )

            print(f"   -> 经过关键词筛选，匹配到 {match_count_for_this_site} 条合适工作")
            print("-" * 50)

        except Exception as e:
            print(f"⚠️ 处理 {url} 时网络请求出错: {e}")
            print("-" * 50)

    if matched_jobs:
        filename = f"Remote_Jobs_{datetime.now().strftime('%Y-%m-%d_%H%M')}.csv"
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["职位名称", "发布时间", "职位链接", "数据来源"])
            writer.writeheader()
            writer.writerows(matched_jobs)

        print(f"\n🎉 筛选完成！共汇总 {len(matched_jobs)} 条优质工作，已保存至: {filename}")
    else:
        print("\n📭 筛选完成。没有找到符合关键词的工作。")


if __name__ == "__main__":
    fetch_and_filter_jobs()
