def sample_inputs_dsplit(op_info, device, dtype, requires_grad):
    return (SampleInput(make_tensor((S, S, S), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=([1, 2, 3],),),
            SampleInput(make_tensor((S, S, 6), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=(2,),),)
