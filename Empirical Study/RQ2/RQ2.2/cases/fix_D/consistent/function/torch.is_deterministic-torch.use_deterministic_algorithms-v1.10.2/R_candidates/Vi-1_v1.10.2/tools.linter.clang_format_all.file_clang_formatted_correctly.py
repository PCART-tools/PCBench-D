async def file_clang_formatted_correctly(
    filename: str,
    semaphore: asyncio.Semaphore,
    verbose: bool = False,
) -> bool:
    """
    Checks if a file is formatted correctly and returns True if so.
    """
    ok = True
    # -style=file picks up the closest .clang-format
    cmd = "{} -style=file {}".format(CLANG_FORMAT_PATH, filename)

    async with semaphore:
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE)
        # Read back the formatted file.
        stdout, _ = await proc.communicate()

    formatted_contents = stdout.decode()
    # Compare the formatted file to the original file.
    with open(filename) as orig:
        orig_contents = orig.read()
        if formatted_contents != orig_contents:
            ok = False
            if verbose:
                print("{} is not formatted correctly".format(filename))

    return ok
