@rpc.functions.async_execution
def async_wrong_type():
    return torch.zeros(2, 2)
