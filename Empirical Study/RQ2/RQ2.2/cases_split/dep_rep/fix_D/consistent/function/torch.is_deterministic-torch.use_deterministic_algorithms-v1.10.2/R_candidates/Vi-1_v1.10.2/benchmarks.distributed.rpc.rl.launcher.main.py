def main():
    r"""
    Runs rpc benchmark once if no argument has multiple entries, and otherwise once for each of the multiple entries.
    Multiple entries is indicated by comma separated values, and may only be done for a single argument.
    Results are printed as well as saved to output file.  In case of multiple entries for a single argument,
    the plot repo can be used to benchmark results on the y axis with each entry on the x axis.
    """
    find_graph_variable(args)

    # run once if no x axis variables
    x_axis_variables = args[args['x_axis_name']] if args.get('x_axis_name') else [None]
    ctx = mp.get_context('spawn')
    queue = ctx.SimpleQueue()
    benchmark_runs = []
    for i, x_axis_variable in enumerate(x_axis_variables):  # run benchmark for every x axis variable
        if len(x_axis_variables) > 1:
            args[args['x_axis_name']] = x_axis_variable  # set x axis variable for this benchmark iteration
        processes = []
        start_time = time.time()
        for rank in range(args['world_size']):
            prc = ctx.Process(
                target=run_worker,
                args=(
                    rank, args['world_size'], args['master_addr'], args['master_port'],
                    args['batch'], args['state_size'], args['nlayers'],
                    args['out_features'], queue
                )
            )
            prc.start()
            processes.append(prc)
        benchmark_run_results = queue.get()
        for process in processes:
            process.join()
        print(f"Time taken benchmark run {i} -, {time.time() - start_time}")
        if args.get('x_axis_name'):
            # save x axis value was for this iteration in the results
            benchmark_run_results[args['x_axis_name']] = x_axis_variable
        benchmark_runs.append(benchmark_run_results)

    report = args
    report['benchmark_results'] = benchmark_runs
    if args.get('x_axis_name'):
        # x_axis_name was variable so dont save a constant in the report for that variable
        del report[args['x_axis_name']]
    with open(args['output_file_path'], 'w') as f:
        json.dump(report, f)
    print_benchmark_results(report)
