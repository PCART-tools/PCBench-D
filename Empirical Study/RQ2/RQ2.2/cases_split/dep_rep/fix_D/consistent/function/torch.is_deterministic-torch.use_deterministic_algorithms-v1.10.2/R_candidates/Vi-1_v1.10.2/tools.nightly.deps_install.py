@timed("Installing dependencies")
def deps_install(deps: List[str], existing_env: bool, env_opts: List[str]) -> None:
    """Install dependencies to deps environment"""
    if not existing_env:
        # first remove previous pytorch-deps env
        cmd = ["conda", "env", "remove", "--yes"] + env_opts
        p = subprocess.run(cmd, check=True)
    # install new deps
    inst_opt = "install" if existing_env else "create"
    cmd = ["conda", inst_opt, "--yes", "--no-deps"] + env_opts + deps
    p = subprocess.run(cmd, check=True)
