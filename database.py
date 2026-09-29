
import os
import aiohttp

DB_URL = os.getenv("DB_URL")

_session: aiohttp.ClientSession | None = None


def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session

async def _get():
    session = _get_session()
    async with session.get(DB_URL) as resp:
        if resp.status != 200:
            return None
        return await resp.json()
