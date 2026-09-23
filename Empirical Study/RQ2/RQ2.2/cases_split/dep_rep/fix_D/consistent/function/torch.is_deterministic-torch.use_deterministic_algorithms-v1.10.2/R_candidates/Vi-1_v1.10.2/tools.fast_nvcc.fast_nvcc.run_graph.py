async def run_graph(
    *,
    env: Dict[str, str],
    commands: List[str],
    graph: Graph,
    gather_data: bool = False,
    save: Optional[str] = None,
) -> List[Result]:
    """
    Return outputs/errors (and optionally time/file info) from commands.
    """
    tasks: List[Awaitable[Result]] = []
    for i, (command, indices) in enumerate(zip(commands, graph)):
        deps = {tasks[j] for j in indices}
        tasks.append(asyncio.create_task(run_command(  # type: ignore[attr-defined]
            command,
            env=env,
            deps=deps,
            gather_data=gather_data,
            i=i,
            save=save,
        )))
    return [await task for task in tasks]
