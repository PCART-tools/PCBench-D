def main(args: List[str]) -> bool:
    # Parse arguments.
    options = parse_args(args)
    # Get clang-format and make sure it is the right binary and it is in the right place.
    ok = get_and_check_clang_format(options.verbose)
    # Invoke clang-format on all files in the directories in the allowlist.
    if ok:
        loop = asyncio.get_event_loop()
        ok = loop.run_until_complete(run_clang_format(options.max_processes, options.diff, options.verbose))

    # We have to invert because False -> 0, which is the code to be returned if everything is okay.
    return not ok
