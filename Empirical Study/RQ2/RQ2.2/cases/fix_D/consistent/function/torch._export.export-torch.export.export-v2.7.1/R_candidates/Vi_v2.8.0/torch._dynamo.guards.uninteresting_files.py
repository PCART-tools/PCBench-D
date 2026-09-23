@functools.cache
def uninteresting_files():
    import torch._dynamo.external_utils
    import torch._dynamo.polyfills

    mods = [torch._dynamo.external_utils, torch._dynamo.polyfills]

    from torch._dynamo.polyfills.loader import POLYFILLED_MODULES

    mods.extend(POLYFILLED_MODULES)

    return {inspect.getfile(m) for m in mods}
