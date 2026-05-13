import httpx


async def get_xkcd() -> dict | None:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get("https://xkcd.com/info.0.json")
        response.raise_for_status()

    data = response.json()
    return {
        "num": data["num"],
        "title": data["title"],
        "alt": data["alt"],
    }
