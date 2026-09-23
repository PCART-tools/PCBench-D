def run_model(model_getter: GetterType, args: Any, task: str) -> List[float]:
    if args.gpu == -1:
        device = torch.device("cpu")

        def noop():
            pass
        do_sync = noop
    else:
        device = torch.device("cuda:{}".format(args.gpu))
        do_sync = torch.cuda.synchronize

    model, inp = model_getter(device)

    v = get_v_for(model, inp, task)
    # Warmup
    run_once(model, inp, task, v)

    elapsed = []
    for it in range(args.num_iters):
        do_sync()
        start = time.time()
        run_once(model, inp, task, v)
        do_sync()
        elapsed.append(time.time() - start)

    return elapsed
