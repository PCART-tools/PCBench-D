def _test_no_segfault():
    dataset = [1, 2, 3]
    num_threads = torch.get_num_threads()
    if num_threads < 4:
        torch.set_num_threads(4)
    else:
        torch.set_num_threads(num_threads)
    mp_ctx = torch.multiprocessing.get_context(method='fork')
    dataloader = DataLoader(dataset, num_workers=1, worker_init_fn=disable_stderr,
                            multiprocessing_context=mp_ctx)
    _ = next(iter(dataloader))
