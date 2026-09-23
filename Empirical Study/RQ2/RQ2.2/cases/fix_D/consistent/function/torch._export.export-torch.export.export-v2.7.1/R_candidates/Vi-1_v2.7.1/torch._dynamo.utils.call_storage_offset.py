def call_storage_offset(x):
    @torch._dynamo.disable(recursive=True)
    def fn(x):
        return x.storage_offset()

    return fn(x)
