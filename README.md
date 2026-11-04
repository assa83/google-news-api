# Google News API – working examples in Python, JavaScript and n8n

Search Google News by keyword, topic or URL in 80+ country editions and get clean JSON with the **real publisher URL** (not the `news.google.com/rss/articles/...` redirect), source and date. Go past the 100-results limit, and switch on monitor mode to receive only the articles that appeared since your last run. A hosted alternative to pygooglenews and GNews.

Powered by the [google-news-scraper](https://apify.com/lagenuina_agency/google-news-scraper) actor on Apify. No browser, no account on Google.

## Example output (real result, shortened)

```json
{
  "title": "Nvidia Requires Cloud Clients to Limit Business With Chinese Customers",
  "source": "marketscreener.com",
  "url": "https://www.marketscreener.com/news/nvidia-requires-cloud-clients-to-limit-business-with-chinese-customers-ce785fd9de81ff21",
  "googleNewsUrl": "https://news.google.com/rss/articles/CBMiwAFBVV95cUxOUzROYnFu...?oc=5",
  "publishedAt": "2026-11-03T09:23:19.000Z",
  "metadata": {
    "keyword": "nvidia",
    "sourceType": "keyword",
    "timeframe": "7d",
    "regionLanguage": "US:en",
    "origin": "google-news"
  }
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py "openai" "nvidia" --timeframe 7d --region GB:en
```

JavaScript: `cd js && npm install && node example.mjs openai nvidia`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/google-news-scraper").call(run_input={
    "keywords": ["openai"],
    "timeframe": "7d",
    "maxArticles": 50,
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["publishedAt"], item["source"], item["title"], item["url"])
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/google-news-scraper').call({ keywords: ['openai'], timeframe: '7d', maxArticles: 50 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~google-news-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"topics": ["BUSINESS"], "region_language": "GB:en", "maxArticles": 20}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/google-news-scraper) (Input tab).

## Use case: news alerts with only new articles

`python/example.py` writes the articles to `news_<date>.csv`. Add `--only-new` and each run returns only what was not returned before, so you can schedule it with cron and pay for new articles only. Use a separate `monitorStoreName` in the input for each independent monitor.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every hour → run the actor with `onlyNew: true` → format each new article → post it to a Slack webhook.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (your keywords) and the Slack webhook URL, then activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```
https://mcp.apify.com/?actors=lagenuina_agency/google-news-scraper
```

Example config (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "google-news-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/google-news-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

Per 1,000 articles, publisher URL included, platform usage included, no start fee:

| Apify plan | Price per 1,000 articles |
|---|---|
| Free | $2.00 |
| Bronze | $1.80 |
| Silver | $1.50 |
| Gold, Platinum, Diamond | $0.80 |

See [lagenuina_agency/google-news-scraper](https://apify.com/lagenuina_agency/google-news-scraper).

## More tools from Quelli di Carne Genuina

- **Ad intelligence:** [Google Ads Transparency](https://github.com/assa83/google-ads-transparency-api) · [Meta Ad Library](https://github.com/assa83/facebook-ad-library-api) · [LinkedIn Ad Library](https://github.com/assa83/linkedin-ad-library-api)
- **Competitor & SEO research:** [Google Trends](https://github.com/assa83/google-trends-api-python) · [Google Play](https://github.com/assa83/google-play-scraper-api)
- **Travel prices:** [Google Hotels](https://github.com/assa83/google-hotels-prices-api) · [Google Flights](https://github.com/assa83/google-flights-api)
- **Content data:** [YouTube Transcript](https://github.com/assa83/youtube-transcript-scraper-api) · [Medium](https://github.com/assa83/medium-scraper-api)

All actors: [apify.com/lagenuina_agency](https://apify.com/lagenuina_agency) · Tutorials: [assa83.github.io](https://assa83.github.io)

## Disclaimer

Independent, not affiliated with Google (not endorsed by Google LLC). It reads only publicly available data. Use it in line with the applicable terms and laws.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
