async def run_clang_format_on_file(
    filename: str,
    semaphore: asyncio.Semaphore,
    verbose: bool = False,
) -> None:
    """
    Run clang-format on the provided file.
    """
    # -style=file picks up the closest .clang-format, -i formats the files inplace.
    cmd = "{} -style=file -i {}".format(CLANG_FORMAT_PATH, filename)
    async with semaphore:
        proc = await asyncio.create_subprocess_shell(cmd)
        _ = await proc.wait()
    if verbose:
        print("Formatted {}".format(filename))
