def sample_inputs_take_along_dim(op_info, device, dtype, requires_grad, **kwargs):
    return (SampleInput(make_tensor((S, S), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=(gather_variable((S, S), 1, S, True, device=device), 0)),

            # `indices` broadcast
            SampleInput(make_tensor((S, S), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=(gather_variable((1, S // 2), 0, S, True, device=device), 1)),

            # `self` broadcast
            SampleInput(make_tensor((1, S), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=(gather_variable((S, S // 2), 0, S, True, device=device), 1)),

            # without `dim` arg
            SampleInput(make_tensor((S, S), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=(gather_variable((S, S // 2), 0, S, True, device=device), )),
            SampleInput(make_tensor((S, S), device, dtype,
                                    low=None, high=None,
                                    requires_grad=requires_grad),
                        args=(gather_variable((S, S // 2), 0, S, True, device=device),)),
            )
