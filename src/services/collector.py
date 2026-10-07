import httpx
import asyncio

async def buscar_dados(url: str) -> dict:

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        print(f"Status code: {r.status_code}")


asyncio.run(buscar_dados('https://boards-api.greenhouse.io/v1/boards/stripe/jobs'))


