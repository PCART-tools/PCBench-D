def parse_args():
    parser = argparse.ArgumentParser(description="test script")

    parser.add_argument(
        "--fail",
        default=False,
        action="store_true",
        help="forces the script to throw a RuntimeError",
    )

    # file is used for assertions
    parser.add_argument(
        "--touch_file_dir",
        type=str,
        help="dir to touch a file with global rank as the filename",
    )
    return parser.parse_args()
