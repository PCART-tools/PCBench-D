    @strobelight(sample_each=10000, stop_at_error=False)
    @torch.compile()
    def work():
        for _ in range(10):
            torch._dynamo.reset()
            for j in range(5):
                torch._dynamo.reset()
                fn(torch.rand(j, j), torch.rand(j, j), torch.rand(j, j))
