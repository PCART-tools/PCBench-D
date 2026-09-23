def packed_fc(model, *args, **kwargs):
    return _FC_or_packed_FC(model, model.net.PackedFC, *args, **kwargs)
