def fc(model, *args, **kwargs):
    return _FC_or_packed_FC(model, model.net.FC, *args, **kwargs)
