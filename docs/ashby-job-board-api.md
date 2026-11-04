# Ashby Job Board API: list a company's jobs with compensation

Ashby's public posting API returns a company's listed jobs, including structured compensation. It needs no key.
Everything below was read live on 2026-11-04.

## Find the slug

It is the path after `jobs.ashbyhq.com/`: `jobs.ashbyhq.com/ashby` gives `ashby`.

## List the jobs

```bash
curl -s "https://api.ashbyhq.com/posting-api/job-board/ashby?includeCompensation=true" \
  | jq '.jobs[] | {title, location, isRemote, workplaceType, employmentType, url: .jobUrl,
                  pay: .compensation.scrapeableCompensationSalarySummary}'
```

The response is `{"jobs": [...], "apiVersion": ...}` (72 jobs for Ashby that day). Each job has `title`, `location`,
`secondaryLocations`, `department`, `team`, `isRemote`, `workplaceType`, `employmentType`, `publishedAt`, `jobUrl`,
`applyUrl` and the description in HTML and plain text.

## Salary: add `includeCompensation=true`

Without the parameter there is no `compensation` object. With it, each job has:

- `compensationTierSummary`: a display line, e.g. "€150K – €250K • Offers Equity • Offers Bonus"
- `scrapeableCompensationSalarySummary`: the salary part only, e.g. "€150K - €250K"
- `compensationTiers[].components[]`: structured parts. A `Salary` component has `minValue`, `maxValue`,
  `currencyCode` and `interval`, e.g. `150000`, `250000`, `EUR`, `1 YEAR`. Equity and bonus are separate components.

```bash
curl -s "https://api.ashbyhq.com/posting-api/job-board/ashby?includeCompensation=true" \
  | jq '.jobs[] | {title, salary: [.compensation.compensationTiers[]?.components[]? | select(.compensationType=="Salary")
        | {min: .minValue, max: .maxValue, currency: .currencyCode, interval}]}'
```

`shouldDisplayCompensationOnJobPostings` says whether the employer shows pay on its own board.

## Many companies, or more than one platform

For one board, the endpoint above is all you need. To pull many companies across Greenhouse, Lever, Ashby, Workable,
Recruitee and Personio into one schema, with salary read from the text when the structured field is empty and only new
or changed jobs on each run, see the [main guide](../README.md). It uses the
[ATS Jobs API with Salary](https://apify.com/flipvo/ats-jobs-scraper) Actor (built by Flipvo LLC, which publishes this repo).
