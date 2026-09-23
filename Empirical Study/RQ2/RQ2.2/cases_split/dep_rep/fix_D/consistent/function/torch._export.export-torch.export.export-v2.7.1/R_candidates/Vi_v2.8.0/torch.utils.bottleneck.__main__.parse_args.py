def parse_args():
    parser = argparse.ArgumentParser(description=descript)
    parser.add_argument('scriptfile', type=str,
                        help='Path to the script to be run. '
                        'Usually run with `python path/to/script`.')
    parser.add_argument('args', type=str, nargs=argparse.REMAINDER,
                        help='Command-line arguments to be passed to the script.')
    return parser.parse_args()
