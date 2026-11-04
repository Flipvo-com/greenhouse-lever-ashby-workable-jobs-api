# Greenhouse Job Board API: list a company's jobs, with salary ranges

Greenhouse publishes every company's open jobs through a free, public Job Board API. It needs no key. Everything below
was read live on 2026-11-04.

## Find the slug

The board token is the last part of the company's Greenhouse careers URL, for example `boards.greenhouse.io/airbnb` or
`job-boards.greenhouse.io/airbnb` gives `airbnb`.

## List the jobs

```bash
curl -s "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs" \
  | jq '.jobs[] | {id, title, location: .location.name, url: .absolute_url, updated_at}'
```

The response is `{"jobs": [...], "meta": {...}}`, with every open job in one response, no paging (`meta.total` was 207
for Airbnb that day). Each job has `id`, `title`, `location.name`, `absolute_url`, `updated_at`, `first_published` and `metadata`.

| Parameter | Adds |
|---|---|
| `content=true` | `content` (the description HTML), `departments`, `offices` |
| `pay_transparency=true` | `pay_input_ranges`: the pay range the employer entered |

## Salary: add `pay_transparency=true`

The pay range is **not returned unless you ask for it**. On 2026-11-04, Airbnb's board returned `pay_input_ranges` on
173 of 207 jobs with `pay_transparency=true`, and on none without it.

```bash
curl -s "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs?pay_transparency=true" \
  | jq '.jobs[] | select(.pay_input_ranges | length > 0)
        | {title, pay: [.pay_input_ranges[] | {min: (.min_cents/100), max: (.max_cents/100), currency: .currency_type, label: .title}]}'
```

Each range has `min_cents`, `max_cents`, `currency_type`, a `title` such as "Canada Annual Pay Range" and a `blurb` (HTML).
Values are in cents, and one job can have several ranges (one per country or level). The same parameter works on a
single job: `/v1/boards/{slug}/jobs/{id}?pay_transparency=true`.

When an employer leaves the pay field empty, the range is often still in the description (`content=true`), as text.

## Notes

- A company that moves off Greenhouse, or renames its board, starts returning 404 for the old slug.
- Track changes by `id` plus `updated_at` between runs. A job that disappears from the list has closed.

## Many companies, or more than one platform

For one board, the endpoint above is all you need. To pull many companies across Greenhouse, Lever, Ashby, Workable,
Recruitee and Personio into one schema, with salary read from the text when the structured field is empty and only new
or changed jobs on each run, see the [main guide](../README.md). It uses the
[ATS Jobs API with Salary](https://apify.com/flipvo/ats-jobs-scraper) Actor (built by Flipvo LLC, which publishes this repo).
