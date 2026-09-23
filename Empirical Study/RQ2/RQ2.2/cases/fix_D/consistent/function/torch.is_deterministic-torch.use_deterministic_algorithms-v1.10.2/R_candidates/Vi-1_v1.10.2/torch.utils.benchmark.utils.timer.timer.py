    def timer() -> float:
        torch.cuda.synchronize()
        return timeit.default_timer()
