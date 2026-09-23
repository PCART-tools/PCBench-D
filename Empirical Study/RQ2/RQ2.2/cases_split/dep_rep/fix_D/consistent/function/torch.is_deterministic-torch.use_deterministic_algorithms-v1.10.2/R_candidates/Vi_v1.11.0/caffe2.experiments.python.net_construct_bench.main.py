def main():
    # TODO: use argv
    parser = argparse.ArgumentParser(
        description="Caffe2: Benchmark for net construction"
    )
    parser.add_argument("--num_gpus", type=int, default=1,
                        help="Number of GPUs.")
    args = parser.parse_args()

    Create(args)
