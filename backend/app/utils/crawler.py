import asyncio
import re
from urllib.parse import urljoin, urlparse
import aiohttp
from bs4 import BeautifulSoup
from typing import Set

async def fetch_html(session: aiohttp.ClientSession, url: str) -> str:
    try:
        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception:
        return ""
    return ""

async def crawl_site(start_url: str, depth: int = 1) -> Set[str]:
    visited: Set[str] = set()
    queue = [(start_url, 0)]
    parsed_root = urlparse(start_url)
    async with aiohttp.ClientSession(headers={"User-Agent": "GEO-Bot/0.1"}) as session:
        while queue:
            url, lvl = queue.pop(0)
            if url in visited or lvl > depth:
                continue
            visited.add(url)
            html = await fetch_html(session, url)
            if not html:
                continue
            if lvl == depth:
                continue
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href.startswith("#"):
                    continue
                new_url = urljoin(url, href)
                parsed = urlparse(new_url)
                if parsed.netloc != parsed_root.netloc:
                    continue
                if new_url not in visited:
                    queue.append((new_url, lvl + 1))
    return visited