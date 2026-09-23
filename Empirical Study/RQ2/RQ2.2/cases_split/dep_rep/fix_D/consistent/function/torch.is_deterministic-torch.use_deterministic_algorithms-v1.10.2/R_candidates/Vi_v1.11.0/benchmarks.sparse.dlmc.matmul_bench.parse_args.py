def parse_args():
    parser = argparse.ArgumentParser(description='matmul benchmark')
    parser.add_argument('--path', type=str, help='DLMC dataset path')
    parser.add_argument('--dataset', type=str, default='magnitude_pruning')
    parser.add_argument('--hidden_size', default=2048, type=int)
    parser.add_argument('--backward_test', action="store_true")
    parser.add_argument('--operation', type=str, help="|".join(OPS_MAP.keys()), default=next(iter(OPS_MAP)))
    parser.add_argument('--with_cuda', action='store_true')
    parser.add_argument('--timer_min_run_time', default=1, type=float)
    return parser
