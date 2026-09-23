def execution_step_with_progress(name, init_net, substeps, rows_read):
    # progress reporter
    report_net = core.Net('report_net')
    report_net.Print([rows_read], [])
    return core.execution_step(
        name,
        substeps,
        report_net=report_net,
        concurrent_substeps=True,
        report_interval=5)
