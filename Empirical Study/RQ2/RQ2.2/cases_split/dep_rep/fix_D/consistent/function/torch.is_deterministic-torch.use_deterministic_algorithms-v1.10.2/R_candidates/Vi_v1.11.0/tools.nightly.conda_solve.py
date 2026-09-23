@timed("Solving conda environment")
def conda_solve(
    name: Optional[str] = None,
    prefix: Optional[str] = None,
    channels: Iterable[str] = ("pytorch-nightly",),
    override_channels: bool = False,
) -> Tuple[List[str], str, str, bool, List[str]]:
    """Performs the conda solve and splits the deps from the package."""
    # compute what environment to use
    if prefix is not None:
        existing_env = True
        env_opts = ["--prefix", prefix]
    elif name is not None:
        existing_env = True
        env_opts = ["--name", name]
    else:
        # create new environment
        existing_env = False
        env_opts = ["--name", "pytorch-deps"]
    # run solve
    if existing_env:
        cmd = [
            "conda",
            "install",
            "--yes",
            "--dry-run",
            "--json",
        ]
        cmd.extend(env_opts)
    else:
        cmd = [
            "conda",
            "create",
            "--yes",
            "--dry-run",
            "--json",
            "--name",
            "__pytorch__",
        ]
    channel_args = _make_channel_args(
        channels=channels, override_channels=override_channels
    )
    cmd.extend(channel_args)
    cmd.extend(SPECS_TO_INSTALL)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    # parse solution
    solve = json.loads(p.stdout)
    link = solve["actions"]["LINK"]
    deps = []
    for pkg in link:
        url = URL_FORMAT.format(**pkg)
        if pkg["name"] == "pytorch":
            pytorch = url
            platform = pkg["platform"]
        else:
            deps.append(url)
    return deps, pytorch, platform, existing_env, env_opts
