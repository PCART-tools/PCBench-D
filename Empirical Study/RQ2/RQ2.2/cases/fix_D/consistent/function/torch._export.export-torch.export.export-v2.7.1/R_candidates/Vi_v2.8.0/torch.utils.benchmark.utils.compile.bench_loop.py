    def bench_loop(
        model: Union[torch.nn.Module, Callable],
        sample_input: Union[torch.Tensor, Any],
        num_iters: int = 5,
        optimizer: Optional[torch.optim.Optimizer] = None,
        loss_fn: Optional[Callable] = None,
    ):
        # Define the statement and setup for the benchmark
        if optimizer and loss_fn:
            # Training mode
            stmt = """
    output = model(sample_input)
    loss = loss_fn(output) if loss_fn else output.sum()
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
            """
        else:
            # Inference mode
            stmt = "model(sample_input)"

        # Create the Timer object
        timer = Timer(
            stmt=stmt,
            globals={"model": model, "sample_input": sample_input, "optimizer": optimizer, "loss_fn": loss_fn},
        )


        result = timer.timeit(number=num_iters)

        # Get the average time per iteration in milliseconds
        avg_time = result.mean * 1000
        return round(avg_time, 2)
