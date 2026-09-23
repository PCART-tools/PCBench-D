async def shell_cmd(
    cmd: Union[str, List[str]],
    env: Optional[Dict[str, Any]] = None,
    redirect: bool = True,
) -> CommandResult:
    if isinstance(cmd, list):
        cmd_str = " ".join(shlex.quote(arg) for arg in cmd)
    else:
        cmd_str = cmd

    proc = await asyncio.create_subprocess_shell(
        cmd_str,
        shell=True,
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE if redirect else None,
        stderr=subprocess.PIPE if redirect else None,
        executable=shutil.which("bash"),
    )
    stdout, stderr = await proc.communicate()

    passed = proc.returncode == 0
    if not redirect:
        return CommandResult(passed, "", "")

    return CommandResult(passed, stdout.decode().strip(), stderr.decode().strip())
