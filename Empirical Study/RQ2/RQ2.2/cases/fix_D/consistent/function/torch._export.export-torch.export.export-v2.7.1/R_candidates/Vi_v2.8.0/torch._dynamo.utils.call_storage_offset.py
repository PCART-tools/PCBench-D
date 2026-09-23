@torch._disable_dynamo
def call_storage_offset(x):
    return x.storage_offset()
