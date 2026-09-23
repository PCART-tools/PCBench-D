def _IsNets(nets_or_steps):
    if isinstance(nets_or_steps, list):
        return all(isinstance(n, core.Net) for n in nets_or_steps)
    else:
        return isinstance(nets_or_steps, core.Net)
