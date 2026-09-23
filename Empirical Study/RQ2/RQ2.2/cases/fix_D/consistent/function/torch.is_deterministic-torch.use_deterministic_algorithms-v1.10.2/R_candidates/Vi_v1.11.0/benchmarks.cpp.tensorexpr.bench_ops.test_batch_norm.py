def test_batch_norm():
    op = F.batch_norm
    print("{:20s} {:20s} {:>10s} {:>10s} {:>10s}".format("op", "shape", "eager", "nnc", "speedup"))
    batch_norm_shapes = [
        [1, 64, 112, 112],
        [1, 256, 14, 14],
        [1, 128, 28, 28],
        [1, 64, 56, 56],
        [1, 512, 7, 7],
        [5, 64, 112, 112],
        [5, 256, 14, 14],
        [5, 128, 28, 28],
        [5, 64, 56, 56],
        [5, 512, 7, 7]]
    for n, c, h, w in batch_norm_shapes:
        x = torch.rand((n, c, h, w))
        y = torch.rand((c))
        z = torch.rand((c))
        traced = torch.jit.trace(lambda x, y, z: op(x, y, z), (x, y, z))

        # Warmup.
        warmup_iters = 8
        for _ in range(warmup_iters):
            op(x, y, z)
            traced(x, y, z)

        # Validate result.
        torch.testing.assert_close(op(x, y, z), traced(x, y, z))

        # Benchmark.
        bench_iters = 100
        teager = timeit.timeit(stmt="op(x, y, z)", globals=locals(), number=bench_iters)
        tjit = timeit.timeit(stmt="traced(x, y, z)", globals=locals(), number=bench_iters)
        print(f"{op.__name__:20s} ({n:>3d}, {c:>3d}, {h:>3d}, {w:>3d}) {teager:10.3f} {tjit:10.3f} {teager/tjit:10.2f}")
