@torch._disable_dynamo
def call_stride(x, i):
    return x.stride(i)
