def print_benchmark_results(report):
    r"""
    Prints benchmark results
    Args:
        report (dict): JSON formatted dictionary containing relevant data on the run of this application
    """
    print("--------------------------------------------------------------")
    print("PyTorch distributed rpc benchmark reinforcement learning suite")
    print("--------------------------------------------------------------")
    for key, val in report.items():
        if key != "benchmark_results":
            print(f'{key} : {val}')

    x_axis_name = report.get('x_axis_name')
    col_width = 7
    heading = ""
    if x_axis_name:
        x_axis_output_label = f'{x_axis_name} |'
        heading += append_spaces(x_axis_output_label, col_width)
    metric_headers = ['agent latency (seconds)', 'agent throughput',
                      'observer latency (seconds)', 'observer throughput']
    percentile_subheaders = ['p50', 'p75', 'p90', 'p95']
    subheading = ""
    if x_axis_name:
        subheading += append_spaces(' ' * (len(x_axis_output_label) - 1), col_width)
    for header in metric_headers:
        heading += append_spaces(header, col_width * len(percentile_subheaders))
        for percentile in percentile_subheaders:
            subheading += append_spaces(percentile, col_width)
    print(heading)
    print(subheading)

    for benchmark_run in report['benchmark_results']:
        run_results = ""
        if x_axis_name:
            run_results += append_spaces(benchmark_run[x_axis_name], max(col_width, len(x_axis_output_label)))
        for metric_name in metric_headers:
            percentile_results = benchmark_run[metric_name]
            for percentile in percentile_subheaders:
                run_results += append_spaces(percentile_results[percentile], col_width)
        print(run_results)
