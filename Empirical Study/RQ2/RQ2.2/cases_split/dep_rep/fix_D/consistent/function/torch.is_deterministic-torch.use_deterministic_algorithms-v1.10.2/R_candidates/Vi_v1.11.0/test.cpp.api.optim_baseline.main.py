def main():
    parser = argparse.ArgumentParser(
        "Produce optimization output baseline from PyTorch"
    )
    parser.add_argument("-i", "--iterations", default=1001, type=int)
    parser.add_argument("-s", "--sample-every", default=100, type=int)
    options = parser.parse_args()

    optimizer_parameter_map = {}
    for optimizer in OPTIMIZERS.keys():
        sys.stderr.write('Evaluating {} ...\n'.format(optimizer))
        optimizer_parameter_map[optimizer] = run(
            optimizer, options.iterations, options.sample_every
        )

    emit(optimizer_parameter_map)
