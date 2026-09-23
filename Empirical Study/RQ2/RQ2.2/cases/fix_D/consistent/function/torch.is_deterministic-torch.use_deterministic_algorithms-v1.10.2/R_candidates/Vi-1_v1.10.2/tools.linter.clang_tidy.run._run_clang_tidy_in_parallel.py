async def _run_clang_tidy_in_parallel(
    commands: List[Tuple[List[str], str]], disable_progress_bar: bool
) -> CommandResult:
    progress_meter = ProgressMeter(
        len(commands),
        f"Processing {len(commands)} clang-tidy jobs",
        disable_progress_bar=disable_progress_bar,
    )

    async def gather_with_concurrency(n: int, tasks: List[Any]) -> Any:
        semaphore = asyncio.Semaphore(n)

        async def sem_task(task: Any) -> Any:
            async with semaphore:
                return await task

        return await asyncio.gather(
            *(sem_task(task) for task in tasks), return_exceptions=True
        )

    async def helper() -> Any:
        def on_completed(result: CommandResult, filename: str) -> None:
            if result.failed():
                msg = str(result) if not VERBOSE else repr(result)
                progress_meter.print(msg)
            progress_meter.update(f"Processed {filename}")

        coros = [
            run_shell_command(cmd, on_completed, filename)
            for (cmd, filename) in commands
        ]
        return await gather_with_concurrency(multiprocessing.cpu_count(), coros)

    results = await helper()
    return sum(results, CommandResult(0, "", ""))
