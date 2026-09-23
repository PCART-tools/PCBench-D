@torch._disable_dynamo
def call_size(x, i):
    return x.size(i)
