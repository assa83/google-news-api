"""Google News to CSV, with real publisher URLs. Add --only-new to get just the articles since the last run.

Usage: python example.py "openai" "nvidia" --timeframe 7d --region GB:en --only-new
"""
import argparse
import csv
import datetime
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/google-news-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("keywords", nargs="+", help="search terms, Google News operators work")
    p.add_argument("--timeframe", default="1d", choices=["1h", "1d", "7d", "30d", "1y", "all"])
    p.add_argument("--region", default="US:en", help="Google News edition, e.g. GB:en, DE:de, IT:it")
    p.add_argument("--max", type=int, default=50, help="max articles per keyword")
    p.add_argument("--only-new", action="store_true", help="monitor mode: skip articles returned by earlier runs")
    a = p.parse_args()

    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={
        "keywords": a.keywords,
        "timeframe": a.timeframe,
        "region_language": a.region,
        "maxArticles": a.max,
        "onlyNew": a.only_new,
    })
    items = client.dataset(run["defaultDatasetId"]).list_items().items

    name = f"news_{datetime.date.today().isoformat()}.csv"
    with open(name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["publishedAt", "keyword", "source", "title", "url"])
        for it in items:
            w.writerow([it["publishedAt"], it["metadata"]["keyword"], it["source"], it["title"], it["url"]])
    print(f"{len(items)} articles -> {name}")


if __name__ == "__main__":
    main()
