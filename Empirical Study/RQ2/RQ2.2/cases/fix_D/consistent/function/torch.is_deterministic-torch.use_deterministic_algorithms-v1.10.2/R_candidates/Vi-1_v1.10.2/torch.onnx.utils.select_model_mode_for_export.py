@contextlib.contextmanager
def select_model_mode_for_export(model, mode):
    if not isinstance(model, torch.jit.ScriptFunction):
        is_originally_training = model.training

        if mode is None:
            mode = TrainingMode.EVAL
            # if the model is in training mode but the user did not specify
            # to export the model in training mode, export the model in inference
            # mode (default) and warn them
            if is_originally_training:
                warnings.warn("You are exporting the model to ONNX while in training mode with "
                              "'train' parameter not specified. The model will default to inference mode export. "
                              "If you wish to export a training amenable ONNX model, specify training=TrainingMode.TRAINING or "
                              "training=TrainingMode.PRESERVE (to preserve the original model state) in torch.onnx.export().")

        # if mode == TrainingMode.EVAL or (mode == TrainingMode.PRESERVE and not is_originally_training) => is_training = False
        is_export_training = False
        # ONNX opset 12 has better support for training amenable models, with updated
        # versions of the dropout and batch_norm operators
        if mode == TrainingMode.TRAINING or (mode == TrainingMode.PRESERVE and is_originally_training):
            from torch.onnx.symbolic_helper import _export_onnx_opset_version
            if _export_onnx_opset_version < 12:
                warnings.warn("You are exporting the model in training mode with onnx opset version {}. "
                              "Opset versions lower than opset 12 will not be able to export nodes such as "
                              "Dropout and BatchNorm correctly.".format(_export_onnx_opset_version))
            is_export_training = True

        from torch.onnx.symbolic_helper import _set_training_mode
        _set_training_mode(is_export_training)
        model.train(is_export_training)
    try:
        yield
    finally:
        if not isinstance(model, torch.jit.ScriptFunction):
            model.train(is_originally_training)
