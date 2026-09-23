@functools.lru_cache(None)
def get_overridable_functions():
    from itertools import chain

    from torch.overrides import get_overridable_functions as get_overridable_functions_

    funcs = set(chain.from_iterable(get_overridable_functions_().values()))
    more = {
        torch.ones,
        torch.ones_like,
        torch.zeros,
        torch.zeros_like,
        torch.empty,
        torch.full,
    }
    funcs.update(more)
    return funcs
