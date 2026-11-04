// Every open job, with salary, from Greenhouse, Lever, Ashby, Workable, Recruitee and Personio boards, in one call.
//   npm install apify-client@2.25.0
//   APIFY_TOKEN=... node example.mjs
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('flipvo/ats-jobs-scraper').call({
    boards: ['airbnb', 'lever:spotify', 'ashby:ashby', 'workable:hirefellows', 'recruitee:channable'],
    keywords: ['engineer'],
    onlyWithSalary: true,
    maxJobsPerBoard: 25,
}, { maxTotalChargeUsd: 1.0 }); // hard budget cap for this run

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const job of items) {
    console.log(job.platform, job.company, job.title, job.salaryMin, job.salaryMax, job.salaryCurrency, job.salarySource);
}
