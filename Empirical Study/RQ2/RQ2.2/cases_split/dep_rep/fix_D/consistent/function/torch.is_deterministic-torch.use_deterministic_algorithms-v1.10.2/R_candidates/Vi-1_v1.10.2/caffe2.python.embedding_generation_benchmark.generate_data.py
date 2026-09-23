def generate_data(T, batch_size, max_seq_length):
    '''
    Fill a queue with input data
    '''
    log.info("Generating T={} batches".format(T))

    generate_input_init_net = core.Net('generate_input_init')
    queue = generate_input_init_net.CreateBlobsQueue(
        [], "inputqueue", num_blobs=1, capacity=T,
    )
    workspace.RunNetOnce(generate_input_init_net)

    generate_input_net = core.Net('generate_input')
    generate_input_net.EnqueueBlobs([queue, "scratch"], ["scratch"])
    np.random.seed(2603)

    for t in range(T):
        if (t % (max(10, T // 10)) == 0):
            log.info("Generating data {}/{}".format(t, T))
        X = np.tile(np.arange(max_seq_length), [batch_size, 1]).transpose()
        workspace.FeedBlob("scratch", X)
        workspace.RunNetOnce(generate_input_net.Proto())

    log.info("Finished data generation")
    return queue
