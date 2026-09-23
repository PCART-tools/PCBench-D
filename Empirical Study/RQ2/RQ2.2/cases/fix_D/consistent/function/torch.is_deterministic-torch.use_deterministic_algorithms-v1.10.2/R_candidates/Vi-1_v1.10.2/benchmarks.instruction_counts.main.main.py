def main(argv: List[str]) -> None:
    work_orders = tuple(
        WorkOrder(label, autolabels, timer_args, timeout=600, retries=2)
        for label, autolabels, timer_args in materialize(BENCHMARKS)
    )

    results = Runner(work_orders).run()
    for work_order in work_orders:
        print(work_order.label, work_order.autolabels, work_order.timer_args.num_threads, results[work_order].instructions)
