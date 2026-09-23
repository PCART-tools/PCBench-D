def _disallow_eval_train(model: GraphModule):
    """
    Disallow calling `model.train()` or `model.eval()` on the given GraphModule.
    This is useful for exported models, where these methods don't actually behave as expected.
    """
    error_message = """
        Calling train() or eval() is not supported for exported models.
        Please call `torch.ao.quantization.move_exported_model_to_train(model)` (or eval) instead.

        If you cannot replace the calls to `model.train()` and `model.eval()`, you may override
        the behavior for these methods by calling `torch.ao.quantization.allow_exported_model_train_eval(model)`,
        which does the above automatically for you. Note that this has limited effect on switching
        behavior between train and eval modes, and should be used only for special ops such as dropout
        and batchnorm.
        """

    def _train(self, mode: bool = True):
        raise NotImplementedError(error_message)

    def _eval(self, mode: bool = True):
        raise NotImplementedError(error_message)

    model.train = types.MethodType(_train, model)  # type: ignore[method-assign]
    model.eval = types.MethodType(_eval, model)  # type: ignore[method-assign]
    return model
