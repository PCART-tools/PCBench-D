async def run_clang_format(
    max_processes: int,
    diff: bool = False,
    verbose: bool = False,
) -> bool:
    """
    Run clang-format to all files in CLANG_FORMAT_ALLOWLIST that match CPP_FILE_REGEX.
    """
    # Check to make sure the clang-format binary exists.
    if not os.path.exists(CLANG_FORMAT_PATH):
        print("clang-format binary not found")
        return False

    # Gather command-line options for clang-format.
    args = [CLANG_FORMAT_PATH, "-style=file"]

    if not diff:
        args.append("-i")

    ok = True

    # Semaphore to bound the number of subprocesses that can be created at once to format files.
    semaphore = asyncio.Semaphore(max_processes)

    # Format files in parallel.
    if diff:
        for f in asyncio.as_completed([file_clang_formatted_correctly(f, semaphore, verbose) for f in get_allowlisted_files()]):
            ok &= await f

        if ok:
            print("All files formatted correctly")
        else:
            print("Some files not formatted correctly")
    else:
        await asyncio.gather(*[run_clang_format_on_file(f, semaphore, verbose) for f in get_allowlisted_files()])

    return ok
