def install(
    *,
    logger: logging.Logger,
    subcommand: str = "checkout",
    branch: Optional[str] = None,
    name: Optional[str] = None,
    prefix: Optional[str] = None,
    channels: Iterable[str] = ("pytorch-nightly",),
    override_channels: bool = False,
) -> None:
    """Development install of PyTorch"""
    deps, pytorch, platform, existing_env, env_opts = conda_solve(
        name=name, prefix=prefix, channels=channels, override_channels=override_channels
    )
    if deps:
        deps_install(deps, existing_env, env_opts)
    pytdir = pytorch_install(pytorch)
    spdir = _site_packages(pytdir.name, platform)
    if subcommand == "checkout":
        checkout_nightly_version(cast(str, branch), spdir)
    elif subcommand == "pull":
        pull_nightly_version(spdir)
    else:
        raise ValueError(f"Subcommand {subcommand} must be one of: checkout, pull.")
    move_nightly_files(spdir, platform)
    write_pth(env_opts, platform)
    pytdir.cleanup()
    logger.info(
        "-------\nPyTorch Development Environment set up!\nPlease activate to "
        f"enable this environment:\n  $ conda activate {env_opts[1]}"
    )
