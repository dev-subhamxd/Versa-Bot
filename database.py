import os
import aiohttp

DB_URL = os.getenv("DATABASE")

_session: aiohttp.ClientSession | None = None


def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session

async def _get(path):
    session = _get_session()
    url = f"{DB_URL}/{path}.json"
    async with session.get(url) as resp:
        if resp.status != 200:
            return None
        return await resp.json()

async def _put(path, value):
    session = _get_session()
    url = f"{DB_URL}/{path}.json"
    async with session.put(url, json=value) as resp:
        return resp.status == 200

async def _delete(path):
    url = f"{DB_URL}/{path}.json"
    session = _get_session()
    async with session.delete(url) as resp:
        return resp.status == 200

# ---------------------------------------------------------------------------------------------------------------

async def register_user(id):
    path = f"users/{id}"
    value = {"core": {"level": 0, "exp": 0, "currency": 0, "points": 0},"imventory": {},"miscellaneous": {}}

    registered_already = "The User already Exists!"
    successfully_registered = "User has been Successfully Registered!"

    if await _get(path) is not None:
        return registered_already
    else:
        await _put(path, value)
        return successfully_registered
