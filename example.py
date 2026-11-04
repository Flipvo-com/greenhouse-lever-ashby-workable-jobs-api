"""Every open job, with salary, from Greenhouse, Lever, Ashby, Workable, Recruitee and Personio boards, in one call.

    pip install "apify-client==2.5.1"
    export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations
    python example.py
"""
import os
from decimal import Decimal

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run = client.actor("flipvo/ats-jobs-scraper").call(
    run_input={
        # A company name, a careers URL, a board URL, or platform:slug. Mix platforms freely.
        "boards": ["airbnb", "lever:spotify", "ashby:ashby", "workable:hirefellows", "recruitee:channable"],
        "keywords": ["engineer"],
        "onlyWithSalary": True,
        "maxJobsPerBoard": 25,
    },
    max_total_charge_usd=Decimal("1.00"),  # hard budget cap for this run
)

for job in client.dataset(run["defaultDatasetId"]).iterate_items():
    lo, hi = job["salaryMin"], job["salaryMax"]
    pay = "-".join(f"{v:,.0f}" for v in (lo, hi) if v is not None)
    pay = f'{pay} {job["salaryCurrency"] or ""}/{job["salaryInterval"] or "?"}'
    print(f'{job["platform"]:10} {job["company"]:12} {job["title"][:48]:48} {pay} ({job["salarySource"]})')
