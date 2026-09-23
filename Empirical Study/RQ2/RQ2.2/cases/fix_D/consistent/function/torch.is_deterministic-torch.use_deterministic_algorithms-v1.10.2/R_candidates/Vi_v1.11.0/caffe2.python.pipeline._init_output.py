def _init_output(output, capacity, global_init_net, global_exit_net):
    if output is None:
        out_queue = queue_util.Queue(
            capacity=(
                capacity if capacity is not None
                else DEFAULT_QUEUE_CAPACITY))
        writer = out_queue.writer()
    elif isinstance(output, Writer):
        assert capacity is None, 'capacity would not be used.'
        out_queue = None
        writer = output
    elif hasattr(output, 'writer'):
        assert capacity is None, 'capacity would not be used.'
        out_queue = output
        writer = output.writer()
    else:
        raise ValueError('output must be a reader, queue or stream.')
    writer.setup_ex(global_init_net, global_exit_net)
    return out_queue, writer
