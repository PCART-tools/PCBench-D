def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add max_tokens_total pragmas to C/C++ source files"
    )
    parser.add_argument(
        "-n",
        "--num-max-tokens",
        default=DEFAULT_MAX_TOKEN_COUNT,
        help="Set the token count to this value",
        type=int,
    )
    parser.add_argument(
        "files", nargs="+", help="Add max_tokens_total pragmas to the specified files"
    )
    parser.add_argument(
        "-i", "--ignore", nargs="+", default=[], help="Ignore the specified files"
    )
    parser.add_argument(
        "-s",
        "--strip",
        action="store_true",
        help="Remove max_tokens_total pragmas from the input files",
    )
    return parser.parse_args()
