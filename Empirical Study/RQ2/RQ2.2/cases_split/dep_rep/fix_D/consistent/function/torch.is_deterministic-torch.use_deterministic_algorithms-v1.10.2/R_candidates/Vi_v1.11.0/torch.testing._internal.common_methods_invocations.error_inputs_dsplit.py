def error_inputs_dsplit(op_info, device, **kwargs):
    err_msg1 = ("torch.dsplit requires a tensor with at least 3 dimension, "
                "but got a tensor with 1 dimensions!")
    si1 = SampleInput(make_tensor((S,),
                                  dtype=torch.float32,
                                  device=device),
                      args=(0,),)
    err_msg2 = (f"torch.dsplit attempted to split along dimension 2, "
                f"but the size of the dimension {S} "
                f"is not divisible by the split_size 0!")
    si2 = SampleInput(make_tensor((S, S, S),
                                  dtype=torch.float32,
                                  device=device),
                      args=(0,),)
    return (ErrorInput(si1, error_type=RuntimeError, error_regex=err_msg1),
            ErrorInput(si2, error_type=RuntimeError, error_regex=err_msg2),)
