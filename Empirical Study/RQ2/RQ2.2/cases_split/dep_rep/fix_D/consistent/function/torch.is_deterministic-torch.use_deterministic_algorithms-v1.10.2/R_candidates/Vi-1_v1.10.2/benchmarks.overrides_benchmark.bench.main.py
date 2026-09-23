def main():
    global NUM_REPEATS
    global NUM_REPEAT_OF_REPEATS

    parser = argparse.ArgumentParser(
        description="Run the __torch_function__ benchmarks."
    )
    parser.add_argument(
        "--nreps",
        "-n",
        type=int,
        default=NUM_REPEATS,
        help="The number of repeats for one measurement.",
    )
    parser.add_argument(
        "--nrepreps",
        "-m",
        type=int,
        default=NUM_REPEAT_OF_REPEATS,
        help="The number of measurements.",
    )
    args = parser.parse_args()

    NUM_REPEATS = args.nreps
    NUM_REPEAT_OF_REPEATS = args.nrepreps

    types = torch.tensor, SubTensor, WithTorchFunction, SubWithTorchFunction

    for t in types:
        tensor_1 = t([1.])
        tensor_2 = t([2.])

        bench_min, bench_std = bench(tensor_1, tensor_2)
        print(
            "Type {0} had a minimum time of {1} us"
            " and a standard deviation of {2} us.".format(
                t.__name__, (10 ** 6 * bench_min), (10 ** 6) * bench_std
            )
        )
