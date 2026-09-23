def _runtime_threads_task(name, group, final_outputs, reader, num_threads,
                          output, capacity):
    node_name = str(Node.current())
    profiler_name = "{0}/{1}/{2}/{3}/{4}".format(
        node_name,
        "pipe",
        name,
        processor_name(input) if input else "NoInput",
        processor_name(output) if output else "NoOutput")

    with Task(name=name, group=group, outputs=final_outputs,
              num_instances=num_threads) as task:
        global_exit_net = core.Net('pipe:exit')
        global_init_net = core.Net('pipe:init')
        reader.setup_ex(global_init_net, global_exit_net)

        init_net = core.Net('pipe:instance:init')
        exit_net = core.Net('pipe:instance:exit')
        read_nets, status, rec = reader.read_record_ex(init_net, exit_net)
        init_net.ConstantFill(
            [], [status],
            shape=[],
            value=False,
            dtype=core.DataType.BOOL
        )

        if rec is not None:
            out_queue, writer = _init_output(
                output, capacity, global_init_net, global_exit_net)
            write_nets, _ = writer.write_record_ex(
                rec, init_net, exit_net, status)
        else:
            out_queue = None
            write_nets = []

        with ops.task_init():
            ops.net(global_init_net)
        with ops.task_instance_init():
            ops.net(init_net)

        timer_start_net = core.Net('timer_start')
        timer = timer_start_net.TimerBegin([], counter_name=profiler_name)
        timer_end_net = core.Net('timer_end')
        timer_end_net.TimerEnd(timer, [])

        ops.net(core.execution_step(
            'body',
            [timer_start_net] + list(read_nets) + list(write_nets) +
            [timer_end_net],
            should_stop_blob=status))
        ops.net(timer_end_net)

        with ops.task_instance_exit():
            ops.net(exit_net)
        with ops.task_exit():
            ops.net(global_exit_net)

    return out_queue, task
