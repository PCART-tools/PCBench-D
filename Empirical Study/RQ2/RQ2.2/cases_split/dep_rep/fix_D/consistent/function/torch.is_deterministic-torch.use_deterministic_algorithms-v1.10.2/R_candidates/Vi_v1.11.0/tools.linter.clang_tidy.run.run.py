def run(options: Any) -> Tuple[CommandResult, List[ClangTidyWarning]]:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_run(options))
