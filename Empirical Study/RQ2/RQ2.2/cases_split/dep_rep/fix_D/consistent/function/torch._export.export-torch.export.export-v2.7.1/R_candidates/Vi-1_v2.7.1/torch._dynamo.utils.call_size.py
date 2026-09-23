def call_size(x, i):
    @torch._dynamo.disable(recursive=True)
    def fn(x, i):
        return x.size(i)

    return fn(x, i)
