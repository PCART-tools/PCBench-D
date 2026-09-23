def parse_args() -> Any:
    from argparse import ArgumentParser
    parser = ArgumentParser("Merge PR/branch into default branch")
    parser.add_argument("--sync-branch", default="sync")
    parser.add_argument("--default-branch", type=str, default="main")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()
