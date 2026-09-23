def parse_args():
    parser = argparse.ArgumentParser(description="test script")
    parser.add_argument(
        "--out_file",
        help="file to write indicating whether this script was launched with torchelastic",
    )
    return parser.parse_args()
