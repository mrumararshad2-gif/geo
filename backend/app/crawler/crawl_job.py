import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from ..database import async_session_maker
from .. import models
from ..utils.crawler import crawl_site

async def run_crawl_job(job_id: int, domain: str, depth: int):
    async with async_session_maker() as session:
        job: models.CrawlJob = await session.get(models.CrawlJob, job_id)
        if not job:
            return
        job.status = models.CrawlStatus.in_progress
        await session.commit()

    urls = await crawl_site(f"http://{domain}", depth)

    async with async_session_maker() as session:
        # fetch site
        job: models.CrawlJob = await session.get(models.CrawlJob, job_id)
        if not job:
            return
        site_id = job.site_id
        existing_urls_result = await session.execute(select(models.Page.url).where(models.Page.site_id == site_id))
        existing_urls = {row[0] for row in existing_urls_result}

        new_pages = []
        for url in urls:
            if url not in existing_urls:
                new_pages.append(models.Page(site_id=site_id, url=url))
        session.add_all(new_pages)
        job.status = models.CrawlStatus.completed
        job.finished_at = datetime.utcnow()
        await session.commit()