def _add_net_to_dict(net_dict, net):
    name = get_net_name(net)
    if name in net_dict:
        assert net_dict[name] is None or net == net_dict[name], (
            'Different nets with same name: ' + name)
        return False
    else:
        net_dict[name] = net if isinstance(net, Net) else None
        return True
