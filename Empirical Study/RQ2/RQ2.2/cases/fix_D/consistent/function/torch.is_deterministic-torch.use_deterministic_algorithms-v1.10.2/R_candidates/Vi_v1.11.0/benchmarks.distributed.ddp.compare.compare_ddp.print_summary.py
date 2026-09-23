def print_summary(buffer_size_to_metrics):
    # metrics: {ddp_option, Metrics}
    # Metrics: step -> [latency]
    for buffer_size, metrics in buffer_size_to_metrics.items():
        assert DDPOption.DDP_CPP_CORE in metrics.keys()
        baseline = metrics.get(DDPOption.DDP_CPP_CORE)
        print(f"=== Summary for buffer_size: {buffer_size}M === ")
        for step in baseline.keys():
            # step takes value from [forward, backward]
            # compute latency for each step into a table, each row is looks like
            # [option, mean, diff, mean, diff, p90, diff, p95, diff, p99, diff]
            data = []
            baseline_latencies = baseline.get(step)
            assert baseline_latencies is not None
            A_baseline = np.array(baseline_latencies)
            for ddp_option, exp_metrics in metrics.items():
                exp_latencies = exp_metrics.get(step)
                assert exp_latencies is not None
                A_exp = np.array(exp_latencies)
                # Yield option, mean, p50, p90, p95, p99 and delta.
                row = [ddp_option]
                row.append(np.mean(A_exp))
                append_delta(row, np.mean(A_baseline), np.mean(A_exp))
                for px in [50, 90, 95, 99]:
                    base = np.percentile(A_baseline, px)
                    exp = np.percentile(A_exp, px)
                    row.append(exp)
                    append_delta(row, base, exp)
                data.append(row)

            # Output buffer_size, step as a table.
            print(tabulate(data,
                           headers=[f"DDP: [{step}]", "Mean", "delta%",
                                    "mean", "delta%", "p90", "delta%",
                                    "p95", "delta%%", "p99", "delta%"]))
            print("\n")
