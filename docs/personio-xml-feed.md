# Personio XML job feed: read a company's open positions

Personio publishes each company's open positions as a public XML feed. It needs no key. Everything below was read live
on 2026-11-04.

## Find the slug

It is the subdomain of the company's Personio jobs page: `lanch.jobs.personio.de` gives `lanch`. Some companies are
on `{slug}.jobs.personio.com` instead of `.de`. The feed is at `/xml` on whichever host the company uses.

## Read the feed

```bash
curl -s "https://lanch.jobs.personio.de/xml" -o feed.xml
```

The root is `<workzag-jobs>` with one `<position>` per job. Each position has `<id>`, `<name>` (the title),
`<office>`, `<additionalOffices>`, `<department>`, `<subcompany>`, `<recruitingCategory>`, `<employmentType>`,
`<seniority>`, `<schedule>`, `<yearsOfExperience>`, `<keywords>`, `<occupation>`, `<occupationCategory>`,
`<createdAt>`, and `<jobDescriptions>`, a list of `<jobDescription>` sections, each with a `<name>` and an HTML
`<value>` in CDATA. Not every position has every element.

```python
import urllib.request, xml.etree.ElementTree as ET

root = ET.fromstring(urllib.request.urlopen("https://lanch.jobs.personio.de/xml").read())
for p in root.iter("position"):
    print(p.findtext("id"), p.findtext("name"), p.findtext("office"), p.findtext("employmentType"))
```

The feed has no job URL. The public page for a position is `https://{slug}.jobs.personio.de/job/{id}`.

## Salary

The feed has no salary element. Pay, when a company states it, is in the `<jobDescription>` text. None of Lanch's 9
positions stated a salary range on 2026-11-04 (one mentioned a 450 EUR payment of "financial support" in its text).

## Many companies, or more than one platform

For one board, the endpoint above is all you need. To pull many companies across Greenhouse, Lever, Ashby, Workable,
Recruitee and Personio into one schema, with salary read from the text when the structured field is empty and only new
or changed jobs on each run, see the [main guide](../README.md). It uses the
[ATS Jobs API with Salary](https://apify.com/flipvo/ats-jobs-scraper) Actor (built by Flipvo LLC, which publishes this repo).
