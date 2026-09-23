def Caffe2EmbeddingGeneration(args):
    T = args.data_size // args.batch_size

    queue = generate_data(T, args.batch_size, args.seq_length)

    embedding_table = None
    if args.implementation == 'table':
        embedding_table = generate_embedding_table(
            args.seq_length,
            args.embedding_size,
        )

    model = create_model(args, queue, embedding_table, args.embedding_size)

    workspace.RunNetOnce(model.param_init_net)
    workspace.CreateNet(model.net)

    start_time = time.time()
    num_iters = T
    total_iters = 0

    # Run the Benchmark
    log.info("------ Warming up ------")
    workspace.RunNet(model.net.Proto().name)

    log.info("------ Starting benchmark ------")
    start_time = time.time()
    last_time = time.time()
    for iteration in range(1, num_iters, args.iters_to_report):
        iters_once = min(args.iters_to_report, num_iters - iteration)
        total_iters += iters_once
        workspace.RunNet(model.net.Proto().name, iters_once)

        new_time = time.time()
        log.info(
            "Iter: {} / {}. Embeddings Generated Per Second: {}k.".format(
                iteration,
                num_iters,
                (iters_once * args.batch_size * args.seq_length) /
                (new_time - last_time) // 100 / 10,
            )
        )
        last_time = new_time

    total_per_sec = (num_iters - 1) * args.batch_size * args.seq_length
    total_per_sec = total_per_sec / (time.time() - start_time) // 100 / 10

    log.info("Done. Total embeddings generated per second " +
             "excluding 1st iteration: {}k".format(total_per_sec))

    return time.time() - start_time
