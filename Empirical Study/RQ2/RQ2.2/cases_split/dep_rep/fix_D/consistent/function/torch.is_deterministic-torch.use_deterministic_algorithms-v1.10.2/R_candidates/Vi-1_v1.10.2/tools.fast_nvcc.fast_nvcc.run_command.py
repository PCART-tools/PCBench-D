async def run_command(
    command: str,
    *,
    env: Dict[str, str],
    deps: Set[Awaitable[Result]],
    gather_data: bool,
    i: int,
    save: Optional[str],
) -> Result:
    """
    Run the command with the given env after waiting for deps.
    """
    for task in deps:
        dep_result = await task
        # abort if a previous step failed
        if 'exit_code' not in dep_result or dep_result['exit_code'] != 0:
            return {}
    if gather_data:
        t1 = time.monotonic()
    proc = await asyncio.create_subprocess_shell(
        command,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    code = cast(int, proc.returncode)
    results: Result = {'exit_code': code, 'stdout': stdout, 'stderr': stderr}
    if gather_data:
        t2 = time.monotonic()
        results['time'] = t2 - t1
        sizes = {}
        for tmp_file in files_mentioned(command):
            if os.path.exists(tmp_file):
                sizes[tmp_file] = os.path.getsize(tmp_file)
            else:
                sizes[tmp_file] = 0
        results['files'] = sizes
    if save:
        dest = pathlib.Path(save) / str(i)
        dest.mkdir()
        for src in map(pathlib.Path, files_mentioned(command)):
            if src.exists():
                shutil.copy2(src, dest / (src.name))
    return results
