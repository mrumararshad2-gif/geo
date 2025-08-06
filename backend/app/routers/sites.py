from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from ..database import get_db
from .. import models, schemas
from ..crawler.crawl_job import run_crawl_job

router = APIRouter(prefix="/sites", tags=["sites"])

@router.post("/", response_model=schemas.SiteRead, status_code=status.HTTP_201_CREATED)
async def create_site(site_in: schemas.SiteCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Site).where(models.Site.domain == site_in.domain))
    site = result.scalars().first()
    if site:
        raise HTTPException(status_code=400, detail="Site already exists")
    site = models.Site(domain=site_in.domain)
    db.add(site)
    await db.commit()
    await db.refresh(site)
    return site

@router.get("/", response_model=list[schemas.SiteRead])
async def list_sites(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Site))
    sites = result.scalars().all()
    return sites

@router.post("/{site_id}/crawl", response_model=schemas.CrawlJobRead, status_code=status.HTTP_202_ACCEPTED)
async def start_crawl(site_id: int, crawl_in: schemas.CrawlJobCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    site = await db.get(models.Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    job = models.CrawlJob(site_id=site_id, depth=crawl_in.depth, status=models.CrawlStatus.pending, started_at=datetime.utcnow())
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # schedule async crawl
    background_tasks.add_task(run_crawl_job, job.id, site.domain, crawl_in.depth)
    return job

@router.get("/{site_id}/pages", response_model=list[schemas.PageRead])
async def list_pages(site_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Page).where(models.Page.site_id == site_id))
    pages = result.scalars().all()
    return pages