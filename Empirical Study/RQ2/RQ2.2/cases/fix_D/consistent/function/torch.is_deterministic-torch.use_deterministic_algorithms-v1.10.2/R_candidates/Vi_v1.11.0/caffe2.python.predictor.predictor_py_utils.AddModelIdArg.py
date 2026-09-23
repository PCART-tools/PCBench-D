def AddModelIdArg(meta_net_def, net_def):
    """Takes the model_id from the predict_net of meta_net_def (if it is
    populated) and adds it to the net_def passed in. This is intended to be
    called on init_nets, as their model_id is not populated by default, but
    should be the same as that of the predict_net
    """
    # Get model_id from the predict_net, assuming it's an integer
    model_id = GetArgumentByName(meta_net_def.predict_net, "model_id")
    if model_id is None:
        return
    model_id = model_id.i

    # If there's another model_id on the net, replace it with the new one
    old_id = GetArgumentByName(net_def, "model_id")
    if old_id is not None:
        old_id.i = model_id
        return

    # Add as an integer argument, this is also assumed above
    arg = net_def.arg.add()
    arg.name = "model_id"
    arg.i = model_id
