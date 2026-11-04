# Workable jobs API: list a company's open jobs without a key

Workable's public widget endpoint returns a company's published jobs. It needs no key and no Workable account.
Everything below was read live on 2026-11-04.

## Find the slug

It is the path after `apply.workable.com/`: `apply.workable.com/hirefellows` gives `hirefellows`.

## List the jobs

```bash
curl -s "https://apply.workable.com/api/v1/widget/accounts/hirefellows" \
  | jq '.jobs[] | {title, city, state, country, telecommuting, employment_type, department, url, published_on}'
```

The response is `{"name", "description", "jobs": [...]}`. Each job has `title`, `shortcode`, `code`, `employment_type`,
`telecommuting`, `department`, `function`, `industry`, `experience`, `education`, `city`, `state`, `country`,
`locations`, `url`, `application_url`, `shortlink`, `published_on` and `created_at`.

| Parameter | Adds |
|---|---|
| `details=true` | `description` (HTML) on every job |

## Salary

The widget response has no pay field. When an employer states pay, it is in the `description` text, so you need
`details=true` and a parser. On 2026-11-04 neither `hirefellows` nor `huggingface` had a job with pay in the text.

## Many companies, or more than one platform

For one board, the endpoint above is all you need. To pull many companies across Greenhouse, Lever, Ashby, Workable,
Recruitee and Personio into one schema, with salary read from the text when the structured field is empty and only new
or changed jobs on each run, see the [main guide](../README.md). It uses the
[ATS Jobs API with Salary](https://apify.com/flipvo/ats-jobs-scraper) Actor (built by Flipvo LLC, which publishes this repo).
