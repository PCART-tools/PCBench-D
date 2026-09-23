    @strobelight(profiler, sample_tags=["something", "another"])
    def work2():
        sum = 0
        for _ in range(100000000):
            sum += 1  # noqa: SIM113
