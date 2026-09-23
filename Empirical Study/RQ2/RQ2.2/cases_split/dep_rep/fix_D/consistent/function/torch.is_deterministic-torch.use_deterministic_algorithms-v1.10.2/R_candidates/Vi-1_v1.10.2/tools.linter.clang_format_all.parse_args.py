def parse_args(args: List[str]) -> argparse.Namespace:
    """
    Parse and return command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Execute clang-format on your working copy changes."
    )
    parser.add_argument(
        "-d",
        "--diff",
        action="store_true",
        default=False,
        help="Determine whether running clang-format would produce changes",
    )
    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    parser.add_argument("--max-processes", type=int, default=50,
                        help="Maximum number of subprocesses to create to format files in parallel")
    return parser.parse_args(args)
