def benchmark_process_group(pg, benchmark, use_ddp_for_single_rank=True):
    torch.manual_seed(pg.rank())
    torch.cuda.manual_seed(pg.rank())

    model = benchmark.create_model()
    data = [(benchmark.generate_inputs(), benchmark.generate_target())]
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(
        model.parameters(),
        0.001,
        momentum=0.9,
        weight_decay=1e-4)
    if use_ddp_for_single_rank or pg.size() > 1:
        model = torch.nn.parallel.DistributedDataParallel(
            model,
            device_ids=[torch.cuda.current_device()],
            broadcast_buffers=False,
            process_group=pg,
            bucket_cap_mb=benchmark.bucket_size)

    measurements = []
    warmup_iterations = 5
    measured_iterations = 10
    for (inputs, target) in (data * (warmup_iterations + measured_iterations)):
        start = time.time()
        output = model(*inputs)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        torch.cuda.synchronize()
        measurements.append(time.time() - start)

    # Throw away measurements for warmup iterations
    return measurements[warmup_iterations:]
