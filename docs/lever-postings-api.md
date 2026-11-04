# Lever Postings API: list a company's jobs as JSON

Lever's public Postings API returns a company's published jobs. It needs no key. Reference:
[lever/postings-api](https://github.com/lever/postings-api). Everything below was read live on 2026-11-04.

## Find the slug

The site name is the first path segment of the company's Lever board: `jobs.lever.co/spotify` gives `spotify`.
Companies on Lever's EU instance use `api.eu.lever.co` instead of `api.lever.co`.

## List the jobs

```bash
curl -s "https://api.lever.co/v0/postings/spotify?mode=json" \
  | jq '.[] | {id, title: .text, location: .categories.location, team: .categories.team,
              commitment: .categories.commitment, url: .hostedUrl, salary: .salaryRange}'
```

Without `mode=json` (or an `Accept: application/json` header) you get HTML. The response is a bare array (86 postings
for Spotify that day). Each posting has `text` (the title), `categories` (`location`, `team`, `department`,
`commitment`, `allLocations`), `hostedUrl`, `applyUrl`, `createdAt` (milliseconds), `workplaceType` and the
description in HTML and plain text.

| Parameter | Effect |
|---|---|
| `skip`, `limit` | Paging, e.g. `?mode=json&skip=0&limit=100` |
| `group` | `location`, `commitment` or `team`: results grouped by that category |
| `location`, `commitment`, `team`, `department`, `level` | Filter by category value; repeat a parameter to OR values |

## Salary

Lever's documented `salaryRange` field (`currency`, `interval`, `min`, `max`) is optional, and many companies leave it
empty. Spotify filled it on none of its 86 postings that day, but its descriptions state the range in text, for example
*Full Stack Engineer - Music*: $132,948 to $189,927 a year. To get that you have to parse `descriptionPlain` and
`additionalPlain`.

## Notes

- `api.lever.co/robots.txt` sets `Crawl-delay: 1`. Wait a second between requests when you pull several companies.
- A posting that drops out of the list has been closed or unpublished.

## Many companies, or more than one platform

For one board, the endpoint above is all you need. To pull many companies across Greenhouse, Lever, Ashby, Workable,
Recruitee and Personio into one schema, with salary read from the text when the structured field is empty and only new
or changed jobs on each run, see the [main guide](../README.md). It uses the
[ATS Jobs API with Salary](https://apify.com/flipvo/ats-jobs-scraper) Actor (built by Flipvo LLC, which publishes this repo).
