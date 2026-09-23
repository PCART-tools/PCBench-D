def parse_args() -> Any:
    from argparse import ArgumentParser
    parser = ArgumentParser("Merge PR into default branch")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--revert", action="store_true")
    parser.add_argument("pr_num", type=int)
    return parser.parse_args()
