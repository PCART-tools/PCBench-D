def _as_tuple(inp, arg_name=None, fn_name=None):
    # Ensures that inp is a tuple of Tensors
    # Returns whether or not the original inp was a tuple and the tupled version of the input
    if arg_name is None and fn_name is None:
        return _as_tuple_nocheck(inp)

    is_inp_tuple = True
    if not isinstance(inp, tuple):
        inp = (inp,)
        is_inp_tuple = False

    for i, el in enumerate(inp):
        if not isinstance(el, torch.Tensor):
            if is_inp_tuple:
                raise TypeError("The {} given to {} must be either a Tensor or a tuple of Tensors but the"
                                " value at index {} has type {}.".format(arg_name, fn_name, i, type(el)))
            else:
                raise TypeError("The {} given to {} must be either a Tensor or a tuple of Tensors but the"
                                " given {} has type {}.".format(arg_name, fn_name, arg_name, type(el)))

    return is_inp_tuple, inp
