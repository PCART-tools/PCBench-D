def make_parser() -> ArgumentParser:
    p = ArgumentParser("nightly")
    # subcommands
    subcmd = p.add_subparsers(dest="subcmd", help="subcommand to execute")
    co = subcmd.add_parser("checkout", help="checkout a new branch")
    co.add_argument(
        "-b",
        "--branch",
        help="Branch name to checkout",
        dest="branch",
        default=None,
        metavar="NAME",
    )
    pull = subcmd.add_parser(
        "pull", help="pulls the nightly commits into the current branch"
    )
    # general arguments
    subps = [co, pull]
    for subp in subps:
        subp.add_argument(
            "-n",
            "--name",
            help="Name of environment",
            dest="name",
            default=None,
            metavar="ENVIRONMENT",
        )
        subp.add_argument(
            "-p",
            "--prefix",
            help="Full path to environment location (i.e. prefix)",
            dest="prefix",
            default=None,
            metavar="PATH",
        )
        subp.add_argument(
            "-v",
            "--verbose",
            help="Provide debugging info",
            dest="verbose",
            default=False,
            action="store_true",
        )
        subp.add_argument(
            "--override-channels",
            help="Do not search default or .condarc channels.",
            dest="override_channels",
            default=False,
            action="store_true",
        )
        subp.add_argument(
            "-c",
            "--channel",
            help="Additional channel to search for packages. 'pytorch-nightly' will always be prepended to this list.",
            dest="channels",
            action="append",
            metavar="CHANNEL",
        )
    return p
