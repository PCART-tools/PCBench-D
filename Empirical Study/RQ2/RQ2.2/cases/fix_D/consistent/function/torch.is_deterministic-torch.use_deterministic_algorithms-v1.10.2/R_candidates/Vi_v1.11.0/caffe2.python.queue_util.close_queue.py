def close_queue(step, *queues):
    close_net = core.Net("close_queue_net")
    for queue in queues:
        close_net.CloseBlobsQueue([queue], 0)
    close_step = core.execution_step("%s_step" % str(close_net), close_net)
    return core.execution_step(
        "%s_wraper_step" % str(close_net),
        [step, close_step])
