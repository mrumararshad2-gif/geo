from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base

class CrawlStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class Site(Base):
    __tablename__ = "site"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    pages = relationship("Page", back_populates="site", cascade="all, delete-orphan")
    crawl_jobs = relationship("CrawlJob", back_populates="site", cascade="all, delete-orphan")
    llms_versions = relationship("LlmsVersion", back_populates="site", cascade="all, delete-orphan")


class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("site.id", ondelete="CASCADE"))
    url = Column(Text, unique=True, nullable=False)
    status_code = Column(Integer)
    html_hash = Column(String(64))
    fetched_at = Column(DateTime)

    site = relationship("Site", back_populates="pages")


class CrawlJob(Base):
    __tablename__ = "crawl_job"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("site.id", ondelete="CASCADE"))
    status = Column(Enum(CrawlStatus), default=CrawlStatus.pending)
    depth = Column(Integer, default=1)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    site = relationship("Site", back_populates="crawl_jobs")


class LlmsVersion(Base):
    __tablename__ = "llms_version"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("site.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String)

    site = relationship("Site", back_populates="llms_versions")