async def run_shell_command(
    cmd: List[str], on_completed: Any = None, *args: Any
) -> CommandResult:
    """Executes a shell command and runs an optional callback when complete"""
    if VERBOSE:
        log("Running: ", " ".join(cmd))

    proc = await asyncio.create_subprocess_shell(
        " ".join(shlex.quote(x) for x in cmd),  # type: ignore[attr-defined]
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    output = await proc.communicate()
    result = CommandResult(
        returncode=proc.returncode if proc.returncode is not None else -1,
        stdout=output[0].decode("utf-8").strip(),
        stderr=output[1].decode("utf-8").strip(),
    )

    if on_completed:
        on_completed(result, *args)

    return result
