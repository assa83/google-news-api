// Google News: latest articles for a few keywords, with the real publisher URL.
// Usage: node example.mjs openai nvidia
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const keywords = process.argv.slice(2).length ? process.argv.slice(2) : ['openai'];
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/google-news-scraper').call({
    keywords,
    timeframe: '1d',
    region_language: 'US:en',
    maxArticles: 20,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const it of items) console.log(`${it.publishedAt.slice(0, 16)} [${it.source}] ${it.title}\n  ${it.url}`);
