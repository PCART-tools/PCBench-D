def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        description="Render xunit output for failed tests",
    )
    parser.add_argument(
        "report_path",
        help="Base xunit reports (single file or directory) to compare to",
    )
    return parser.parse_args()
