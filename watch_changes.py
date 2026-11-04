"""Run on a schedule (cron, GitHub Actions, Apify Schedules): only new and changed jobs come back,
plus a free `closed` row for each job that left the board since the last run.

    APIFY_TOKEN=... python watch_changes.py
"""
import os
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
# The first run has nothing to compare with, so it is a full pull: every job comes back as `new` and is billed.
# Later runs bill only new and changed jobs. The cap below holds on every run.
run = client.actor("flipvo/ats-jobs-scraper").call(
    run_input={"boards": ["airbnb", "lever:spotify"], "onlyChanges": True},
    max_total_charge_usd=Decimal("1.00"),  # hard budget cap for this run
)
for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(job["changeStatus"], job["company"], job["title"], job["url"])  # new / changed / closed
