def parse_args():
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument('-b', '--benchmarks', nargs='+',
                        default=ALL_BENCHMARKS.keys(),
                        help='benchmarks to run (default: %(default)s))')
    return parser.parse_args()
