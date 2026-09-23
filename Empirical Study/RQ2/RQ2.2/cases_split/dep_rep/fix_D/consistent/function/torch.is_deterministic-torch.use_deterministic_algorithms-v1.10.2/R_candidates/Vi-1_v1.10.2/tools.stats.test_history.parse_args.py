def parse_args(raw: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        __file__,
        description=description(),
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        '--mode',
        choices=['columns', 'multiline'],
        help='output format',
        default='columns',
    )
    parser.add_argument(
        '--pytorch',
        help='path to local PyTorch clone',
        default='.',
    )
    parser.add_argument(
        '--ref',
        help='starting point (most recent Git ref) to display history for',
        default='master',
    )
    parser.add_argument(
        '--delta',
        type=int,
        help='minimum number of hours between commits',
        default=0,
    )
    parser.add_argument(
        '--sha-length',
        type=int,
        help='length of the prefix of the SHA1 hash to show',
        default=40,
    )
    parser.add_argument(
        '--digits',
        type=int,
        help='(columns) number of digits to display before the decimal point',
        default=4,
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='(multiline) ignore listed jobs, show all jobs for each commit',
    )
    parser.add_argument(
        '--file',
        help='name of the file containing the test',
    )
    parser.add_argument(
        '--suite',
        help='name of the suite containing the test',
    )
    parser.add_argument(
        '--test',
        help='name of the test',
        required=True
    )
    parser.add_argument(
        '--job',
        help='names of jobs to display columns for, in order',
        action='append',
        default=[],
    )
    args = parser.parse_args(raw)

    args.jobs = None if args.all else args.job
    # We dont allow implicit or empty "--jobs", unless "--all" is specified.
    if args.jobs == []:
        parser.error('No jobs specified.')

    return args
