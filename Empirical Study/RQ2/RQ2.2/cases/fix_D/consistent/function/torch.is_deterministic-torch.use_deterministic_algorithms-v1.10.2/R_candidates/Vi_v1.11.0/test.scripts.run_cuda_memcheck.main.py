async def main():
    tasks = [asyncio.ensure_future(run1(i)) for i in range(args.nproc)]
    for t in tasks:
        await t
