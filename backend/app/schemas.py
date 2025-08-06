from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from enum import Enum

class CrawlStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class SiteCreate(BaseModel):
    domain: str

class SiteRead(BaseModel):
    id: int
    domain: str
    created_at: datetime

    class Config:
        orm_mode = True

class CrawlJobCreate(BaseModel):
    depth: Optional[int] = 1

class CrawlJobRead(BaseModel):
    id: int
    status: CrawlStatus
    depth: int
    started_at: Optional[datetime]
    finished_at: Optional[datetime]

    class Config:
        orm_mode = True

class PageRead(BaseModel):
    id: int
    url: HttpUrl
    status_code: Optional[int]
    fetched_at: Optional[datetime]

    class Config:
        orm_mode = True