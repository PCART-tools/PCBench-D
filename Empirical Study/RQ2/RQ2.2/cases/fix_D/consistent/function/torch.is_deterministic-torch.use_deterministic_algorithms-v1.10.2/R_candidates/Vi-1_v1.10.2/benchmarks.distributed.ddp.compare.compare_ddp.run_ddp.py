def run_ddp(rank, world_size, epochs, ddp_option, buffer_size_in_M, warmup_iterations=20):
    print(f'Invoked run_ddp rank {rank}')
    assert epochs > warmup_iterations

    # Setup
    print("setting up ... ")
    setup(rank, world_size)
    torch.manual_seed(rank)
    torch.cuda.manual_seed(rank)
    device = torch.device('cuda:%d' % rank)
    print('setup done')

    # Create ResNet50 module and wrap in DDP module.
    pg = dist.distributed_c10d._get_default_group()
    model = models.resnet50().to(device)
    ddp_model = create_ddp_model(model, rank, pg, ddp_option, buffer_size_in_M)
    assert ddp_model is not None

    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)

    # Container to hold: event -> list of events in milliseconds
    MODEL_FORWARD = "forward"
    MODEL_BACKWARD = "backward"
    metrics = {MODEL_FORWARD: [], MODEL_BACKWARD: []}

    for epoch in range(epochs):
        if epoch % 10 == 0:
            print(f'Epoch {epoch}/{epochs} ...')

        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)

        # TODO(bowangbj): Switch to real training set from ImageNet.
        inputs = torch.rand([32, 3, 224, 224], device=device)
        labels = torch.rand([32, 1000], device=device)

        # Forward
        start.record()
        outputs = ddp_model(inputs)
        loss = loss_fn(outputs, labels)

        end.record()
        torch.cuda.synchronize()
        if epoch >= warmup_iterations:
            metrics[MODEL_FORWARD].append(start.elapsed_time(end))

        # Backward
        start.record()
        loss.backward()
        # Reduce all grad, this is needed for non-DDP_CPP_CORE since the hook
        # for all_reduce does not exist yet.
        if ddp_option != DDPOption.DDP_CPP_CORE:
            ddp_model.all_reduce_grads()
        end.record()
        torch.cuda.synchronize()
        if epoch >= warmup_iterations:
            metrics[MODEL_BACKWARD].append(start.elapsed_time(end))

        # Optimization
        optimizer.step()
        optimizer.zero_grad()

    if rank == 0:
        print(f"\nMetrics for GPU {rank}, ddp_option={ddp_option}, buffer_size={buffer_size_in_M}M")
        print(f"Skipped {warmup_iterations} CUDA warmpup iterations. ")
        for step, elapsed_milliseconds in metrics.items():
            A = np.array(elapsed_milliseconds)
            print(' {N} iterations, {step}, mean={mean} ms, median={median} ms, p90={p90} ms, p99={p99} ms'.format(
                N=len(A), step=step, mean=np.mean(A),
                median=np.percentile(A, 50), p90=np.percentile(A, 90),
                p99=np.percentile(A, 99)))

        # Serialize the raw data to be used to compute summary. Didn't choose to
        # maintain a global object holding the metrics b/c mp.spawn tries to
        # fork all the arguments before spawning new process thus it's infeasible
        # save global states in an object.
        serialize(buffer_size_in_M, ddp_option, rank, metrics)
