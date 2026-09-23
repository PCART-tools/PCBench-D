def _AppendNets(nets_or_steps, *nets):
    nets_or_steps = _MakeList((nets_or_steps,))
    nets = _MakeList(nets)
    if _IsNets(nets_or_steps):
        return nets_or_steps + nets
    else:
        return nets_or_steps + [Do('append', nets)]
