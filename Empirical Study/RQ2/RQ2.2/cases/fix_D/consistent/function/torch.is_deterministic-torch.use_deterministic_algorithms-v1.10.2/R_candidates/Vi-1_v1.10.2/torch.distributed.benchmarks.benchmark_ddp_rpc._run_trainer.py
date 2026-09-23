def _run_trainer(emb_rref_list, rank):
    r"""
   Each trainer runs a forward pass which involves an embedding lookup on the
   8 parameter servers and running nn.Linear locally. During the backward pass,
   DDP is responsible for aggregating the gradients for the dense part
   (nn.Linear) and distributed autograd ensures gradients updates are
   propagated to the parameter servers.
   """

    # Setup the model.
    model = HybridModel(emb_rref_list, rank)

    # Retrieve all model parameters as rrefs for DistributedOptimizer.

    # Retrieve parameters from all embedding tables for the current trainer.
    model_parameter_rrefs = []
    for ind, emb_rref in enumerate(emb_rref_list):
        ps_name = "ps{}".format(ind)
        model_parameter_rrefs.extend(
            rpc.rpc_sync(ps_name, _retrieve_embedding_parameters, args=(emb_rref,))
        )

    # model.parameters() only includes local parameters.
    for param in model.parameters():
        model_parameter_rrefs.append(RRef(param))

    # Setup distributed optimizer
    opt = DistributedOptimizer(optim.SGD, model_parameter_rrefs, lr=0.05)

    criterion = torch.nn.CrossEntropyLoss()

    def get_next_batch(rank):
        for _ in range(10):
            num_indices = random.randint(20, 50)
            indices = torch.LongTensor(num_indices).random_(0, NUM_EMBEDDINGS)

            # Generate offsets.
            offsets = []
            start = 0
            batch_size = 0

            while start < num_indices:
                offsets.append(start)
                start += random.randint(1, 10)
                batch_size += 1

            offsets_tensor = torch.LongTensor(offsets)
            target = torch.LongTensor(batch_size).random_(8).cuda(rank)

            yield indices, offsets_tensor, target

    measurements = []
    # Include warm-up cycles during training
    for epoch in range(100 + WARMUP_CYCLES):
        start = time.time()
        batch_size = 0

        # create distributed autograd context
        for indices, offsets, target in get_next_batch(rank):
            batch_size += len(target)

            with dist_autograd.context() as context_id:
                output = model(indices, offsets)
                loss = criterion(output, target)

                # Run distributed backward pass
                dist_autograd.backward(context_id, [loss])

                # Run distributed optimizer. Gradients propagated all the way to the parameter servers
                opt.step(context_id)

                # Not necessary to zero grads as each iteration creates a different
                # distributed autograd context which hosts different grads

        measurements.append(time.time() - start)
        # print("Training done for epoch {}".format(epoch))

    # Throw away warm-up measurements
    measurements = measurements[WARMUP_CYCLES:]
    return rank, measurements, batch_size
