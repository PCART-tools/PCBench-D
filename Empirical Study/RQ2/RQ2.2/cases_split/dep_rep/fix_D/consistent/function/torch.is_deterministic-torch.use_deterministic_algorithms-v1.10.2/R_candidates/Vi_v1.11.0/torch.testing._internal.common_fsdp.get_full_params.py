def get_full_params(model, recurse=True):
    if recurse:
        # get all params for any nested FSDP instances.
        for module in model.modules():
            if isinstance(module, FullyShardedDataParallel):
                get_full_params(module, recurse=False)
    else:
        torch.cuda.synchronize()
        model._rebuild_full_params()
        torch.cuda.synchronize()
        if model.module.flat_param is not None:
            model.module._unflatten_params()
