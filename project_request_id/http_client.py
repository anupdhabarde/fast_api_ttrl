import asyncio
import httpx


async def request():
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000")


async def run():
    await asyncio.gather(*[request() for _ in range(4)])


if __name__ == "__main__":
    asyncio.run(run())
