def _PrependNets(nets_or_steps, *nets):
    nets_or_steps = _MakeList((nets_or_steps,))
    nets = _MakeList(nets)
    if _IsNets(nets_or_steps):
        return nets + nets_or_steps
    else:
        return [Do('prepend', nets)] + nets_or_steps
