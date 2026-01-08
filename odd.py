import asyncio
import time

import aiohttp


async def fetch_data(session, url):
    print(f"Starting task: {url}")
    async with session.get(url) as response:
        await asyncio.sleep(1)  # Simulating a delay
        data = await response.json()
        print(f"Completed task: {url}")
        return data


async def main():
    urls = [
        "https://api.github.com/",
        "https://api.spacexdata.com/v4/launches/latest",
        "https://jsonplaceholder.typicode.com/todos/1",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for result in results:
            print(result)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print(f"Total time taken: {time.time() - start_time} seconds")
