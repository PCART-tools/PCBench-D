def train_convnext_example():
    device_type = "cuda"
    world_size = int(os.environ["WORLD_SIZE"])
    mesh = init_device_mesh(device_type, (world_size,))
    rank = mesh.get_rank()

    in_shape = [7, 3, 512, 1024]
    output_shape = [7, 1000]

    torch.manual_seed(12)
    model = ConvNeXt(
        depths=[3, 3, 27, 3],
        dims=[256, 512, 1024, 2048],
        drop_path_rate=0.0,
        num_classes=1000,
    ).to(device_type)
    model = distribute_module(model, mesh, _conv_fn, input_fn=None, output_fn=None)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, amsgrad=False)

    x = torch.randn(*in_shape).to(device_type).requires_grad_()
    y_target = (
        torch.empty(output_shape[0], dtype=torch.long)
        .random_(output_shape[1])
        .to(device_type)
    )
    x = distribute_tensor(x, mesh, [Shard(3)])
    y_target = distribute_tensor(y_target, mesh, [Replicate()])

    # warm up
    y = model(x)
    loss = criterion(y, y_target)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    torch.cuda.synchronize()

    forward_time = 0.0
    backward_time = 0.0
    start = time.time()
    for _ in range(ITER_TIME):
        t1 = time.time()
        y = model(x)
        torch.cuda.synchronize()
        t2 = time.time()

        loss = criterion(y, y_target)
        optimizer.zero_grad()

        t3 = time.time()
        loss.backward()
        torch.cuda.synchronize()
        t4 = time.time()

        optimizer.step()

        forward_time += t2 - t1
        backward_time += t4 - t3
    torch.cuda.synchronize()
    end = time.time()
    max_reserved = torch.cuda.max_memory_reserved()
    max_allocated = torch.cuda.max_memory_allocated()
    print(
        f"rank {rank}, {ITER_TIME} iterations, "
        f"average latency {(end - start) / ITER_TIME * 1000:10.2f} ms"
    )
    print(
        f"rank {rank}, forward {forward_time / ITER_TIME * 1000:10.2f} ms, "
        f"backward {backward_time / ITER_TIME * 1000:10.2f} ms"
    )
    print(
        f"rank {rank}, max reserved {max_reserved / 1024 / 1024 / 1024:8.2f} GiB, "
        f"max allocated {max_allocated / 1024 / 1024 / 1024:8.2f} GiB"
    )
    dist.destroy_process_group()
