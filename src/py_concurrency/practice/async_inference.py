import asyncio
import random
import time

async def fake_inference_request(i: int, sem: asyncio.Semaphore): 
    async with sem:
        start = time.perf_counter()

        delay = random.uniform(0.05, 0.3)
        await asyncio.sleep(delay)

        end = time.perf_counter()
        latency = end - start

        return latency

async def run_benchmark(num_requests: int, concurrency: int):
    sem = asyncio.Semaphore(concurrency)

    print(f"Running benchmark: num_requests={num_requests}, concurrency={concurrency}")
    start = time.perf_counter()

    tasks = [
        asyncio.create_task(fake_inference_request(i, sem)) for i in range(num_requests)
    ]

    latencies = await asyncio.gather(*tasks)
    end = time.perf_counter()

    total_time = end - start

    avg_latency = sum(latencies) / len(latencies)

    print(f"Total wall-clock time: {total_time:.3f}s")
    print(f"Average per-request latency: {avg_latency:.3f}s")
    print(f"Throughput: {num_requests / total_time:.2f} requests/sec")


if __name__ == "__main__":
    # For reproducible randomness in demos, you might set a seed:
    # random.seed(42)
    asyncio.run(run_benchmark(num_requests=100, concurrency=10))
