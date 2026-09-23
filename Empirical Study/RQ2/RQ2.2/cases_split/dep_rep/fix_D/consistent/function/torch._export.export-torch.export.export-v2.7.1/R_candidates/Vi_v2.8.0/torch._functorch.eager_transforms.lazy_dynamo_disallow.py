def lazy_dynamo_disallow(func):
    import torch._dynamo

    return torch._dynamo.disallow_in_graph(func)
