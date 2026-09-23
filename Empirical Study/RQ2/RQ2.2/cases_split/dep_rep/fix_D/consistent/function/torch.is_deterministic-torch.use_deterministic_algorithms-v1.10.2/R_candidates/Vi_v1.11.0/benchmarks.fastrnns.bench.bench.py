def bench(rnn_runners, group_name, print_json=False, sep=' ', **params):
    print_stderr(print_header(sep=sep))
    results = {}
    for name, creator, context in rnn_runners:
        with context():
            try:
                result = trainbench(name, creator, **params)
                # Replace the value of info_fwd and info_bwd to None
                result_with_no_info = result._replace(
                    info_fwd='None', info_bwd='None')
                print_stderr(pretty_print(result_with_no_info, sep=sep))
                results[name] = result
            except Exception as e:
                if not print_json:
                    raise

    return {
        group_name: {k: {"avg": v.avg_fwd, "std": v.std_fwd, "info": v.info_fwd} for k, v in results.items()},
        group_name + '-backward': {k: {"avg": v.avg_bwd, "std": v.std_bwd, "info": v.info_bwd} for k, v in results.items()},
    }
