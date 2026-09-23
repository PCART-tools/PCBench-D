def add_arguments_oss(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument(
        "--run-only",
        help="only run certain test(s), for example: atest test_nn.py.",
        nargs="*",
        default=None,
    )

    return parser
