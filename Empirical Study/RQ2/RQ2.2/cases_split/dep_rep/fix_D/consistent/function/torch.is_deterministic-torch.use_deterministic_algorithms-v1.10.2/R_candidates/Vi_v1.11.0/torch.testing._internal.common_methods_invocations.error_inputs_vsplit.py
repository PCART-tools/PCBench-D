def error_inputs_vsplit(op_info, device, **kwargs):
    err_msg1 = ("torch.vsplit requires a tensor with at least 2 dimension, "
                "but got a tensor with 1 dimensions!")
    si1 = SampleInput(make_tensor((S,),
                                  dtype=torch.float32,
                                  device=device),
                      args=(0,),)
    err_msg2 = (f"torch.vsplit attempted to split along dimension 0, "
                f"but the size of the dimension {S} "
                f"is not divisible by the split_size 0!")
    si2 = SampleInput(make_tensor((S, S, S),
                                  dtype=torch.float32,
                                  device=device),
                      args=(0,),)
    return (ErrorInput(si1, error_type=RuntimeError, error_regex=err_msg1),
            ErrorInput(si2, error_type=RuntimeError, error_regex=err_msg2),)
