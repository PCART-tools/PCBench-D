def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Export a JSON of slow test cases in PyTorch unit test suite')
    parser.add_argument(
        '-f',
        '--filename',
        nargs='?',
        type=str,
        default=SLOW_TESTS_FILE,
        const=SLOW_TESTS_FILE,
        help='Specify a file path to dump slow test times from previous S3 stats. Default file path: .pytorch-slow-tests.json',
    )
    parser.add_argument(
        '--ignore-small-diffs',
        nargs='?',
        type=float,
        const=RELATIVE_DIFFERENCE_THRESHOLD,
        help='Compares generated results with stats/slow-tests.json in pytorch/test-infra. If the relative differences '
             'between test times for each test are smaller than the threshold and the set of test cases have not '
             'changed, we will export the stats already in stats/slow-tests.json. Else, we will export the calculated '
             'results. The default threshold is 10%.',
    )
    return parser.parse_args()
