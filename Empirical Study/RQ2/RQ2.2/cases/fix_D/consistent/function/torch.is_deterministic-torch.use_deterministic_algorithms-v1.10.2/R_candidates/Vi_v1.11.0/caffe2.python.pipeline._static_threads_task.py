def _static_threads_task(name, group, final_outputs, reader, num_threads,
                         output, capacity):
    node_name = str(Node.current())
    profiler_name = "{0}/{1}/{2}/{3}/{4}".format(
        node_name,
        "pipe",
        name,
        processor_name(input) if input else "NoInput",
        processor_name(output) if output else "NoOutput")

    with Task(name=name, group=group, outputs=final_outputs) as task:
        global_exit_net = core.Net('exit')
        global_init_net = core.Net('init')
        reader.setup_ex(global_init_net, global_exit_net)

        out_queue = None
        writer = None

        steps = []
        for thread_id in range(num_threads):
            with NetBuilder(name='t:%d' % thread_id) as nb:
                init_net = core.Net('init')
                exit_net = core.Net('exit')
                read_nets, status, rec = reader.read_record_ex(
                    init_net, exit_net)
                init_net.ConstantFill(
                    [], [status],
                    shape=[],
                    value=False,
                    dtype=core.DataType.BOOL
                )

                if rec is not None:
                    if writer is None:
                        # hack so that the out queue gets the right name prefix
                        # (otherwise they would be prefixed with the thread id)
                        with NetBuilder(_fullname=task.name):
                            out_queue, writer = _init_output(
                                output, capacity, global_init_net,
                                global_exit_net)
                    write_nets, _ = writer.write_record_ex(
                        rec, init_net, exit_net, status)
                else:
                    write_nets = []

                timer_start_net = core.Net('timer_start')
                timer = timer_start_net.TimerBegin([], counter_name=profiler_name)
                timer_end_net = core.Net('timer_end')
                timer_end_net.TimerEnd(timer, [])

                ops.net(init_net)
                ops.net(core.execution_step(
                    'body',
                    [timer_start_net] + list(read_nets) + list(write_nets) +
                    [timer_end_net],
                    should_stop_blob=status))
                ops.net(timer_end_net)
                ops.net(exit_net)
            steps.append(core.to_execution_step(nb))
        ops.net(global_init_net)
        ops.net(core.execution_step('body', steps, concurrent_substeps=True))
        ops.net(global_exit_net)
    return out_queue, task
