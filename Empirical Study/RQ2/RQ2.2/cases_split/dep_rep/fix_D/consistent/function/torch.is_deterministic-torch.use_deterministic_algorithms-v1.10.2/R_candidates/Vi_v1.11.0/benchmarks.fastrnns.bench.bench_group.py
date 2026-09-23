def bench_group(model_list, bench_name, bench_group, bench_args):
    print_stderr('Benchmarking {}s...'.format(bench_name))
    nn_results = bench(get_nn_runners(*model_list), bench_group, **bench_args)
    print_stderr('')
    return nn_results
