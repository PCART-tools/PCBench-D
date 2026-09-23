def _move_exported_model_to_train(model: torch.fx.GraphModule):
    """
    Move an exported GraphModule to train mode.

    This is equivalent to model.train() but only for certain special ops like dropout, batchnorm.
    QAT users should call this before performing training on the model.

    This call is idempotent; if the model is already in train mode, nothing will happen.
    """
    is_training = getattr(model, _EXPORTED_TRAINING_ATTR, False)
    if is_training:
        return model
    setattr(model, _EXPORTED_TRAINING_ATTR, True)
    _replace_dropout(model, train_to_eval=False)
    _replace_batchnorm(model, train_to_eval=False)
    return model
