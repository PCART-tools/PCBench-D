def main(args: Optional[Sequence[str]] = None) -> None:
    """Main entry point"""
    global LOGGER
    p = make_parser()
    ns = p.parse_args(args)
    ns.branch = getattr(ns, "branch", None)
    status = check_in_repo()
    status = status or check_branch(ns.subcmd, ns.branch)
    if status:
        sys.exit(status)
    channels = ["pytorch-nightly"]
    if ns.channels:
        channels.extend(ns.channels)
    with logging_manager(debug=ns.verbose) as logger:
        LOGGER = logger
        install(
            subcommand=ns.subcmd,
            branch=ns.branch,
            name=ns.name,
            prefix=ns.prefix,
            logger=logger,
            channels=channels,
            override_channels=ns.override_channels,
        )
