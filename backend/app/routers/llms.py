from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..database import get_db
from .. import models, schemas
from ..utils.llms import validate_llms

router = APIRouter(prefix="/sites/{site_id}/llms", tags=["llms"])

@router.post("/", response_model=schemas.LlmsVersionRead, status_code=status.HTTP_201_CREATED)
async def create_llms(site_id: int, llms_in: schemas.LlmsVersionCreate, db: AsyncSession = Depends(get_db)):
    if not validate_llms(llms_in.content):
        raise HTTPException(status_code=400, detail="Invalid LLMS.txt syntax")
    site = await db.get(models.Site, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    version = models.LlmsVersion(site_id=site_id, content=llms_in.content, created_by=llms_in.created_by)
    db.add(version)
    await db.commit()
    await db.refresh(version)
    return version

@router.get("/", response_model=list[schemas.LlmsVersionRead])
async def list_versions(site_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.LlmsVersion).where(models.LlmsVersion.site_id == site_id).order_by(models.LlmsVersion.created_at.desc()))
    return result.scalars().all()

@router.get("/{version_id}", response_model=schemas.LlmsVersionRead)
async def get_version(site_id: int, version_id: int, db: AsyncSession = Depends(get_db)):
    version = await db.get(models.LlmsVersion, version_id)
    if not version or version.site_id != site_id:
        raise HTTPException(status_code=404, detail="Version not found")
    return version