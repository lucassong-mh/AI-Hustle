#!/usr/bin/env python3
import json
import os
import re
import urllib.request
import urllib.parse
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_eastmoney_news():
    import time
    trace_id = str(int(time.time() * 1000))
    url = f"https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=350&order=1&needInteractData=0&page_index=1&page_size=20&req_trace={trace_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://finance.eastmoney.com/",
    }
    req = urllib.request.Request(url, headers=headers)
    news_list = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("data", {}).get("list", [])
            for item in items:
                news_list.append({
                    "title": item.get("title", ""),
                    "time": item.get("showTime", ""),
                    "source": "东方财富",
                    "url": item.get("url", ""),
                })
    except Exception as e:
        print(f"  东方财富新闻获取失败: {e}")
    return news_list


def fetch_sina_finance_news():
    url = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&num=20&versionNumber=1.2.4"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    news_list = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("result", {}).get("data", [])
            for item in items:
                news_list.append({
                    "title": item.get("title", ""),
                    "time": item.get("ctime", ""),
                    "source": "新浪财经",
                    "url": item.get("url", ""),
                })
    except Exception as e:
        print(f"  新浪财经新闻获取失败: {e}")
    return news_list


def fetch_cls_telegraph():
    url = "https://www.cls.cn/api/subject/list?app=CailianpressWeb&os=web&sv=7.7.5"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    news_list = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("data", [])
            for item in items:
                news_list.append({
                    "title": item.get("title", ""),
                    "time": item.get("ctime", ""),
                    "source": "财联社",
                    "url": "",
                })
    except Exception as e:
        print(f"  财联社新闻获取失败: {e}")
    return news_list


def extract_hot_topics(news_list):
    keyword_weights = {
        "政策": 5, "利好": 4, "涨停": 4, "龙头": 4, "突破": 3,
        "新高": 3, "大涨": 3, "改革": 3, "降息": 4, "降准": 4,
        "刺激": 3, "支持": 3, "批复": 3, "新能源": 3, "芯片": 3,
        "人工智能": 4, "AI": 4, "机器人": 3, "低空经济": 3,
        "军工": 2, "半导体": 3, "消费": 2, "医药": 2,
        "利空": -3, "下跌": -2, "暴跌": -3, "风险": -1,
        "违规": -2, "退市": -3, "ST": -3,
        "war": -3, "冲突": -3, "tariff": -2, "关税": -2,
        "sanctions": -2, "制裁": -2, "Fed": 3, "美联储": 3,
        "rate": 2, "利率": 2, "recession": -3, "衰退": -3,
        "inflation": -2, "通胀": -2, "earnings": 2, "财报": 2,
        "China": 3, "regulation": -2, "监管": -1,
    }

    hot_sectors = {}
    for news in news_list:
        title = news.get("title", "")
        if not title:
            continue
        for kw, weight in keyword_weights.items():
            if kw in title:
                if kw not in hot_sectors:
                    hot_sectors[kw] = {"count": 0, "weight": 0, "titles": []}
                hot_sectors[kw]["count"] += 1
                hot_sectors[kw]["weight"] += weight
                hot_sectors[kw]["titles"].append(title)

    sorted_topics = sorted(hot_sectors.items(), key=lambda x: x[1]["weight"], reverse=True)
    return sorted_topics


def fetch_cnbc_news():
    proxy_handler = urllib.request.ProxyHandler({
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897",
    })
    opener = urllib.request.build_opener(proxy_handler)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"
    req = urllib.request.Request(url, headers=headers)
    news_list = []
    try:
        with opener.open(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", content)
            if not titles:
                titles = re.findall(r"<title>(.*?)</title>", content)
            for title in titles[:20]:
                title = title.strip()
                if title in ("US Top News and Analysis", "CNBC"):
                    continue
                news_list.append({
                    "title": title,
                    "time": "",
                    "source": "CNBC",
                    "url": "",
                })
    except Exception as e:
        print(f"  CNBC新闻获取失败: {e}")
    return news_list


def fetch_google_news_china():
    proxy_handler = urllib.request.ProxyHandler({
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897",
    })
    opener = urllib.request.build_opener(proxy_handler)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    url = "https://news.google.com/rss/search?q=china+stock+market&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers=headers)
    news_list = []
    try:
        with opener.open(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            titles = re.findall(r"<title>(.*?)</title>", content)
            for title in titles[:20]:
                title = title.strip()
                if title.startswith('"') or title == "Google News":
                    continue
                news_list.append({
                    "title": title,
                    "time": "",
                    "source": "GoogleNews",
                    "url": "",
                })
    except Exception as e:
        print(f"  Google News获取失败: {e}")
    return news_list


def fetch_marketwatch():
    proxy_handler = urllib.request.ProxyHandler({
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897",
    })
    opener = urllib.request.build_opener(proxy_handler)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    url = "https://feeds.content.dowjones.io/public/rss/mw_topstories"
    req = urllib.request.Request(url, headers=headers)
    news_list = []
    try:
        with opener.open(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
            for item in items[:20]:
                title_match = re.search(r"<title><!\[CDATA\[(.*?)\]\]></title>", item)
                if not title_match:
                    title_match = re.search(r"<title>(.*?)</title>", item)
                if title_match:
                    title = title_match.group(1).strip()
                    if title == "MarketWatch.com - Top Stories":
                        continue
                    news_list.append({
                        "title": title,
                        "time": "",
                        "source": "MarketWatch",
                        "url": "",
                    })
    except Exception as e:
        print(f"  MarketWatch获取失败: {e}")
    return news_list


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print("=== 获取国内财经新闻 ===")

    print("  正在获取东方财富新闻...")
    em_news = fetch_eastmoney_news()
    print(f"  获取到 {len(em_news)} 条")

    print("  正在获取新浪财经新闻...")
    sina_news = fetch_sina_finance_news()
    print(f"  获取到 {len(sina_news)} 条")

    print("  正在获取财联社电报...")
    cls_news = fetch_cls_telegraph()
    print(f"  获取到 {len(cls_news)} 条")

    print("\n=== 获取国际财经新闻 ===")

    print("  正在获取CNBC国际新闻...")
    cnbc_news = fetch_cnbc_news()
    print(f"  获取到 {len(cnbc_news)} 条")

    print("  正在获取Google News中国股市...")
    google_news = fetch_google_news_china()
    print(f"  获取到 {len(google_news)} 条")

    print("  正在获取MarketWatch...")
    mw_news = fetch_marketwatch()
    print(f"  获取到 {len(mw_news)} 条")

    domestic_news = em_news + sina_news + cls_news
    international_news = cnbc_news + google_news + mw_news
    all_news = domestic_news + international_news

    print(f"\n=== 共获取 {len(all_news)} 条新闻 ===")

    hot_topics = extract_hot_topics(all_news)

    result = {
        "date": today,
        "total_news": len(all_news),
        "domestic_count": len(domestic_news),
        "international_count": len(international_news),
        "news": all_news[:80],
        "hot_topics": [{"keyword": k, "count": v["count"], "weight": v["weight"], "sample_titles": v["titles"][:3]} for k, v in hot_topics[:20]],
    }

    filepath = os.path.join(OUTPUT_DIR, f"news_{today}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"  新闻数据已保存到 {filepath}")

    if hot_topics:
        print("\n=== 今日热点关键词 ===")
        for kw, info in hot_topics[:10]:
            print(f"  [{kw}] 出现{info['count']}次 权重{info['weight']}  例: {info['titles'][0][:40]}...")


if __name__ == "__main__":
    main()