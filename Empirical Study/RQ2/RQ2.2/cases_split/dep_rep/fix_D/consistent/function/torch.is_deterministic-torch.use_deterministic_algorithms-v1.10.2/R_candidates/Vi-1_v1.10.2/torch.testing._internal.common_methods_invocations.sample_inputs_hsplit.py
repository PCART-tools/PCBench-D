def sample_inputs_hsplit(op_info, device, dtype, requires_grad):
    return (SampleInput(make_tensor((6,), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=(2,),),
            SampleInput(make_tensor((S, S, S), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=([1, 2, 3],),),)
