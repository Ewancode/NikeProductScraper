# Nike product scraper

A Scrapy spider that extracts product name, price and URL from Nike's UK
men's t-shirt listings. Self-directed work, written while teaching myself
Scrapy from scratch.

## What it does

`nike/spiders/nikespider.py` issues a `SplashRequest` so that the listing page
is rendered before parsing — Nike's product grid is built client-side, so a
plain HTTP response contains no products. It then selects each
`div.product-card` and yields:

| Field | Selector |
|---|---|
| Product Name | `div.product-card__title::text` |
| Product Price | `div[data-testid="product-price"]::text` |
| Product URL | `a.product-card__img-link-overlay::attr(href)` (resolved with `response.urljoin`) |

## Running it

```bash
pip install -r requirements.txt

# Splash runs as a container and must be up before the spider
docker run -d -p 8050:8050 scrapinghub/splash

scrapy crawl nikespider -o products.csv
```

## Known limitations

Listed rather than hidden:

- **Splash is not wired into `settings.py`.** `SPLASH_URL` and the
  `scrapy_splash` downloader middlewares still need adding before
  `SplashRequest` will work.
- `ROBOTSTXT_OBEY` is left at `True`, which is the correct default but means
  the spider will not crawl paths the target disallows.
- `items.py` defines no fields and `pipelines.py` is the generated
  pass-through — output goes straight to the feed exporter rather than through
  a validated item schema or a database.
- One retailer only. Extending to a second would mean a new spider plus a
  normalisation step, since field names and page structure differ per site.

## Next

The obvious extension is a second retailer and a matching step to identify the
same garment across two differently-worded listings.
