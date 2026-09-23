def _move_exported_model_to_eval(model: torch.fx.GraphModule):
    """
    Move an exported GraphModule to eval mode.

    This is equivalent to model.eval() but only for certain special ops like dropout, batchnorm.
    QAT users should call this before performing inference on the model.

    This call is idempotent; if the model is already in eval mode, nothing will happen.
    """
    is_training = getattr(model, _EXPORTED_TRAINING_ATTR, True)
    if not is_training:
        return model
    setattr(model, _EXPORTED_TRAINING_ATTR, False)
    _replace_dropout(model, train_to_eval=True)
    _replace_batchnorm(model, train_to_eval=True)
    return model
