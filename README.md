# Get every Greenhouse, Lever, Ashby, Workable, Recruitee and Personio job, with salary, in one API call

Most tech companies post their jobs on an applicant-tracking system (ATS) such as **Greenhouse**, **Lever**, **Ashby**,
**Workable**, **Recruitee** or **Personio**. All six publish open jobs through a free public API, but each one returns a different shape, and
salary is usually buried in the description text. This repo shows two ways to get them:

1. **Do it yourself** with the free public endpoints (below). This is the right choice for one company and one platform.
2. **One call for any mix of companies**, with a single schema across all six platforms, salary read from the text when
   the structured field is empty, and a "what changed since last run" mode. That uses the
   [ATS Jobs API with Salary](https://apify.com/flipvo/ats-jobs-scraper) Actor on Apify.

> Disclosure: the Actor is built and maintained by Flipvo LLC, which also publishes this repo. You don't need it to
> use the public endpoints in option 1.

## 1. The free public endpoints

No key needed. Each returns JSON, except Personio's XML feed. All six returned 200 on 2026-11-04.

| Platform | Endpoint | Example board |
|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs` (add `?content=true` for descriptions) | `airbnb` |
| Lever | `https://api.lever.co/v0/postings/{slug}?mode=json` | `spotify` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true` | `ashby` |
| Workable | `https://apply.workable.com/api/v1/widget/accounts/{slug}` | `hirefellows` |
| Recruitee | `https://{slug}.recruitee.com/api/offers/` | `channable` |
| Personio | `https://{slug}.jobs.personio.de/xml` (XML; some companies are on `.jobs.personio.com`) | `lanch` |

```bash
curl -s https://boards-api.greenhouse.io/v1/boards/airbnb/jobs | jq '.jobs[] | {title, location: .location.name, url: .absolute_url}'
```

What you still have to build yourself: finding which platform and slug a company uses, mapping six schemas (one of them XML) into one,
pulling the salary out of the description when there's no structured field, pacing requests (Lever's `robots.txt`
asks for a 1-second crawl delay), retrying 429s, and working out what's new or closed since yesterday.

## 2. One call for all six

```bash
pip install "apify-client==2.5.1"
export APIFY_TOKEN=...   # free account: https://console.apify.com/settings/integrations
python example.py
```

[`example.py`](example.py) (a Node version is in [`example.mjs`](example.mjs)):

```python
run = client.actor("flipvo/ats-jobs-scraper").call(
    run_input={
        "boards": ["airbnb", "lever:spotify", "ashby:ashby", "workable:hirefellows", "recruitee:channable"],
        "keywords": ["engineer"],
        "onlyWithSalary": True,
        "maxJobsPerBoard": 25,
    },
    max_total_charge_usd=Decimal("1.00"),  # hard budget cap for this run
)
for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    ...
```

A `boards` entry can be a company name (`airbnb`), a careers-page URL, a board URL
(`jobs.lever.co/spotify`), or `platform:slug`. You can mix platforms in one run.

### What one row looks like

From a real run on 2026-11-04 with the first four boards above and `maxJobsPerBoard: 5` (all 15 rows are in [`sample-output.json`](sample-output.json)):

```json
{
  "platform": "lever",
  "company": "spotify",
  "title": "Full Stack Engineer - Music",
  "location": "New York, NY",
  "salaryMin": 132948,
  "salaryMax": 189927,
  "salaryCurrency": "USD",
  "salaryInterval": "year",
  "salarySource": "text",
  "changeStatus": "unchanged",
  "url": "https://jobs.lever.co/spotify/9899871a-4307-4367-9f74-039569d7a650"
}
```

**No Workable rows in that sample:** on 2026-11-04, neither `hirefellows` nor `huggingface` (both on Workable) had a job with a published salary, so `onlyWithSalary` filtered them all out. A run on `hirefellows` without the salary filter returns its jobs normally; 3 real rows from it are in [`sample-output-workable.json`](sample-output-workable.json).

**Recruitee and Personio:** a run on `recruitee:channable` and `personio:lanch` (6 real rows in
[`sample-output-recruitee-personio.json`](sample-output-recruitee-personio.json)) gave Channable's structured salaries,
for example *Senior Engineering Manager - Core*, 100,000-120,000 EUR/year. Lanch's Personio feed published no pay that
day, so its rows have no salary.

Spotify fills in no structured pay field on Lever, so this range was read from the job text. The print loop in `example.py`, run over that dataset, shows (in part):

```
greenhouse Airbnb       Machine Learning Engineer, Assistance Engineerin 162,000-186,000 USD/year (structured)
lever      spotify      Full Stack Engineer - Music                      132,948-189,927 USD/year (text)
ashby      ashby        Engineering Manager - Americas                   225,000-325,000 USD/year (structured)
```

`salarySource` is `structured` when the employer filled in the pay field, and `text` when the range was read from
the description (for example `$150,000 - $200,000` or `$75/hr - $90/hr`). The Actor never estimates. A job with no
published pay has no salary.

### Track changes on a schedule

[`watch_changes.py`](watch_changes.py) sets `onlyChanges: true`. Each run returns only jobs that are new or changed
since the previous run of the same boards, plus a free `closed` row for every job that has left the board. Run it from
cron, GitHub Actions or an Apify Schedule to feed a job board, a Slack alert or a hiring-signal list.

## Use it from an AI agent (MCP)

Apify's hosted MCP server can expose the Actor as one tool to Claude, Cursor or any other MCP client. Add this server
URL to the client and sign in with your Apify account:

```
https://mcp.apify.com/?actors=flipvo/ats-jobs-scraper
```

The tool is listed as `flipvo--ats-jobs-scraper`. No argument is required, so the agent can call it at once and add
`boards`, `keywords` or `onlyChanges` as it needs. Setup details: [Apify MCP docs](https://docs.apify.com/integrations/mcp).

## Pricing

The Actor charges per job delivered. Filtered-out jobs and `closed` rows are free. The current price is on the
[Store page](https://apify.com/flipvo/ats-jobs-scraper). Pass `max_total_charge_usd` (Python) or `maxTotalChargeUsd`
(Node) to cap what any single run can cost.

## License

MIT for the code in this repo. Job data belongs to the employers who posted it.
