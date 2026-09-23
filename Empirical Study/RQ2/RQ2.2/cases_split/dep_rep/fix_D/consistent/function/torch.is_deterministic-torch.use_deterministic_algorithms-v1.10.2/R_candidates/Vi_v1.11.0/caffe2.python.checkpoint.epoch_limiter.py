def epoch_limiter(job, num_epochs):
    """
    Creates a task that will output True when a given
    number of epochs has finished.
    """
    with job.init_group:
        init_net = core.Net('epoch_counter_init')
        counter = init_net.CreateCounter([], init_count=num_epochs - 1)
        Task(step=init_net)

    with job.epoch_group:
        epoch_net = core.Net('epoch_countdown')
        finished = epoch_net.CountDown(counter)
        output = Task(step=epoch_net, outputs=finished).outputs()[0]
    job.add_stop_condition(output)
