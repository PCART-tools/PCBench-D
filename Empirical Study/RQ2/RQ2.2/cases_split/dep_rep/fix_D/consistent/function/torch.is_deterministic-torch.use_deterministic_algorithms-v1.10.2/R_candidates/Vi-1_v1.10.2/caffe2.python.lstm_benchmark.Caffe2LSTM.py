def Caffe2LSTM(args):
    T = args.data_size // args.batch_size

    input_blob_shape = [args.seq_length, args.batch_size, args.input_dim]
    queue, label_queue, entry_counts = generate_data(T // args.seq_length,
                                       input_blob_shape,
                                       args.hidden_dim,
                                       args.fixed_shape)

    workspace.FeedBlob(
        "seq_lengths",
        np.array([args.seq_length] * args.batch_size, dtype=np.int32)
    )

    model, output = create_model(args, queue, label_queue, input_blob_shape)

    workspace.RunNetOnce(model.param_init_net)
    workspace.CreateNet(model.net)

    start_time = time.time()
    num_iters = T // args.seq_length
    total_iters = 0

    # Run the Benchmark
    log.info("------ Warming up ------")
    workspace.RunNet(model.net.Proto().name)

    if (args.gpu):
        log.info("Memory stats:")
        stats = utils.GetGPUMemoryUsageStats()
        log.info("GPU memory:\t{} MB".format(stats['max_total'] / 1024 / 1024))

    log.info("------ Starting benchmark ------")
    start_time = time.time()
    last_time = time.time()
    for iteration in range(1, num_iters, args.iters_to_report):
        iters_once = min(args.iters_to_report, num_iters - iteration)
        total_iters += iters_once
        workspace.RunNet(model.net.Proto().name, iters_once)

        new_time = time.time()
        log.info(
            "Iter: {} / {}. Entries Per Second: {}k.".format(
                iteration,
                num_iters,
                np.sum(entry_counts[iteration:iteration + iters_once]) /
                (new_time - last_time) // 100 / 10,
            )
        )
        last_time = new_time

    log.info("Done. Total EPS excluding 1st iteration: {}k {}".format(
         np.sum(entry_counts[1:]) / (time.time() - start_time) // 100 / 10,
         " (with RNN executor)" if args.rnn_executor else "",
    ))

    if (args.gpu):
        log.info("Memory stats:")
        stats = utils.GetGPUMemoryUsageStats()
        log.info("GPU memory:\t{} MB".format(stats['max_total'] / 1024 / 1024))
        if (stats['max_total'] != stats['total']):
            log.warning(
                "Max usage differs from current total usage: {} > {}".
                format(stats['max_total'], stats['total'])
            )
            log.warning("This means that costly deallocations occurred.")

    return time.time() - start_time
