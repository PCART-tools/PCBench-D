def test_sparse_coo_and_csr(m, nnz, test_count):
    start = Event(enable_timing=True)
    stop = Event(enable_timing=True)

    coo, csr = gen_sparse_coo_and_csr((m, m), nnz)
    vector = torch.randn(m, dtype=torch.double)

    times = []
    for _ in range(test_count):
        start.record()
        coo.matmul(vector)
        stop.record()

        times.append(start.elapsed_time(stop))

    coo_mean_time = sum(times) / len(times)

    times = []
    for _ in range(test_count):
        start.record()
        csr.matmul(vector)
        stop.record()
        times.append(start.elapsed_time(stop))

    csr_mean_time = sum(times) / len(times)

    return coo_mean_time, csr_mean_time
