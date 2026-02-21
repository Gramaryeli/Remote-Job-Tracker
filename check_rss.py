import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib3

# 1. 屏蔽 SSL 安全警告，防止终端被红色信息刷屏
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 2. 网站列表
target_urls = [
    "https://weworkremotely.com/",
    "https://remoteok.com/",
    "https://dribbble.com/jobs",
    "https://www.flexjobs.com/",
    "https://www.upwork.com/",
    "https://remotive.com/",
    "https://www.toptal.com/",
    "https://en.freelance.com/",
    "https://www.topcoder.com/",
    "https://www.workingnomads.com/jobs",
    "https://www.fiverr.com/",
    "https://www.vorka.ai/",
    "https://jobgether.com/",
    "https://www.workable.com/",
]


def find_rss_feeds(url):
    """探测指定网站中的标准 RSS/Atom 链接"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    # 3. 核心配置：根据你的 Clash Verge 截图设置 7897 端口
    proxies = {
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897",
    }

    try:
        # verify=False 是解决 ValueError 和 SSLError 的关键
        response = requests.get(
            url, headers=headers, proxies=proxies, verify=False, timeout=15
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        rss_links = []

        # 查找所有标准 RSS 或 Atom 标签
        for link in soup.find_all(
            "link", type=["application/rss+xml", "application/atom+xml"]
        ):
            href = link.get("href")
            if href:
                full_url = urllib.parse.urljoin(url, href)
                rss_links.append(full_url)

        return rss_links

    except Exception as e:
        # 这里捕捉所有异常，方便你查看具体哪个网站连接有问题
        print(f"[-] 访问 {url} 时出错: {e}")
        return []


if __name__ == "__main__":
    print("🚀 开始探测远程工作网站的 RSS 订阅源...")
    print(f"📡 当前代理配置: http://127.0.0.1:7897 (Verify: False)")
    print("-" * 50)

    results_found = 0

    for site in target_urls:
        feeds = find_rss_feeds(site)
        if feeds:
            results_found += 1
            print(f"[+] 成功！在 {site} 发现以下 RSS 源:")
            for feed in feeds:
                print(f"    ⭐ {feed}")
        else:
            print(f"[-] 未找到: {site} (无标准 RSS 标签或被反爬)")
        print("-" * 50)

    print(f"\n✅ 探测完成！共在 {results_found} 个网站中发现可用源。")
    print("💡 请复制带 [+] 的链接，下一步我们将使用这些链接自动筛选职位。")
