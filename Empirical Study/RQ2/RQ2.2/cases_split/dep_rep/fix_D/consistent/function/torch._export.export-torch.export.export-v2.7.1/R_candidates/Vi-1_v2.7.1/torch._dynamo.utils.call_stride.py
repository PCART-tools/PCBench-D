def call_stride(x, i):
    @torch._dynamo.disable(recursive=True)
    def fn(x, i):
        return x.stride(i)

    return fn(x, i)
