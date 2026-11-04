"""Run on a schedule (cron, GitHub Actions, Apify Schedules): only new and changed jobs come back,
plus a free `closed` row for each job that left the board since the last run.

    APIFY_TOKEN=... python watch_changes.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("flipvo/ats-jobs-scraper").call(
    run_input={"boards": ["airbnb", "lever:spotify"], "onlyChanges": True}
)
for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(job["changeStatus"], job["company"], job["title"], job["url"])  # new / changed / closed
