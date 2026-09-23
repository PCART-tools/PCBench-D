def generate_data(T, shape, num_labels, fixed_shape):
    '''
    Fill a queue with input data
    '''
    log.info("Generating T={} sequence batches".format(T))

    generate_input_init_net = core.Net('generate_input_init')
    queue = generate_input_init_net.CreateBlobsQueue(
        [], "inputqueue", num_blobs=1, capacity=T,
    )
    label_queue = generate_input_init_net.CreateBlobsQueue(
        [], "labelqueue", num_blobs=1, capacity=T,
    )

    workspace.RunNetOnce(generate_input_init_net)
    generate_input_net = core.Net('generate_input')

    generate_input_net.EnqueueBlobs([queue, "scratch"], ["scratch"])
    generate_input_net.EnqueueBlobs([label_queue, "label_scr"], ["label_scr"])
    np.random.seed(2603)

    entry_counts = []
    for t in range(T):
        if (t % (max(10, T // 10)) == 0):
            print("Generating data {}/{}".format(t, T))
        # Randomize the seqlength
        random_shape = (
            [np.random.randint(1, shape[0])] + shape[1:]
            if t > 0 and not fixed_shape else shape
        )
        X = np.random.rand(*random_shape).astype(np.float32)
        batch_size = random_shape[1]
        L = num_labels * batch_size
        labels = (np.random.rand(random_shape[0]) * L).astype(np.int32)
        workspace.FeedBlob("scratch", X)
        workspace.FeedBlob("label_scr", labels)
        workspace.RunNetOnce(generate_input_net.Proto())
        entry_counts.append(random_shape[0] * random_shape[1])

    log.info("Finished data generation")

    return queue, label_queue, entry_counts
