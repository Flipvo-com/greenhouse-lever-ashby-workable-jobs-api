# Recruitee Careers Site API: list a company's job offers with salary

Every Recruitee careers site exposes its published offers as JSON. It needs no key. Everything below was read live on
2026-11-04.

## Find the slug

It is the subdomain of the company's Recruitee site: `channable.recruitee.com` gives `channable`.

## List the offers

```bash
curl -s "https://channable.recruitee.com/api/offers/" \
  | jq '.offers[] | {id, title, location, city, country, remote, hybrid, department, url: .careers_url, salary, published_at}'
```

The response is `{"offers": [...]}` (12 offers for Channable that day). Each offer has `title`, `slug`, `department`,
`location`, `city`, `country_code`, `remote`, `hybrid`, `on_site`, `employment_type_code`, `experience_code`,
`min_hours_per_week`, `max_hours_per_week`, `description` and `requirements` (HTML), `careers_url`,
`careers_apply_url`, `published_at`, `updated_at` and `close_at`.

## Salary

`salary` is a structured object when the employer fills it in, e.g. `{"min": "2976", "max": "4252", "period": "month",
"currency": "EUR"}`. Note that `min` and `max` are **strings**, and `period` varies (`month` and `year` both appeared on Channable's board), so
convert both before you compare offers. An offer without pay still has the object, with every field `null`.
One Channable offer that day had `"min": "0", "max": "0"` (DKK): treat zeros as no salary.

## Many companies, or more than one platform

For one board, the endpoint above is all you need. To pull many companies across Greenhouse, Lever, Ashby, Workable,
Recruitee and Personio into one schema, with salary read from the text when the structured field is empty and only new
or changed jobs on each run, see the [main guide](../README.md). It uses the
[ATS Jobs API with Salary](https://apify.com/flipvo/ats-jobs-scraper) Actor (built by Flipvo LLC, which publishes this repo).
