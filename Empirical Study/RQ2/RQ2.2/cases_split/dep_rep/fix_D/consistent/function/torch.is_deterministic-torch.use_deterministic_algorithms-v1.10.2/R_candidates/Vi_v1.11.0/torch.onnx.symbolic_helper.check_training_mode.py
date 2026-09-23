def check_training_mode(op_train_mode, op_name):
    global _training_mode
    op_train_mode = True if op_train_mode == 1 else False
    if _training_mode is not None and op_train_mode != _training_mode:
        op_mode = "training " if op_train_mode else "inference"
        training_mode = "training " if _training_mode else "inference"
        # setting the model mode could result in op_mode != _training_mode
        # if the model is a FuncModule. In this case we warn the user of
        # the state and export depending on op_mode
        # This is to support use-cases of fixing certain layer weights
        # in training.
        warnings.warn("ONNX export mode is set to " + training_mode +
                      " mode, but operator " + op_name + " is set to " +
                      op_mode + " mode. The operators will be exported in " +
                      op_mode + ", as specified by the functional operator.")
