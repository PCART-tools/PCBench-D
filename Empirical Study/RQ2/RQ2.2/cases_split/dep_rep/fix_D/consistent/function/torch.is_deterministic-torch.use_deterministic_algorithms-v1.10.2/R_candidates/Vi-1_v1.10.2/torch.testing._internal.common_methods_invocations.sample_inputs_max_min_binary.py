def sample_inputs_max_min_binary(op_info, device, dtype, requires_grad, **kwargs):
    inputs = []
    args_for_binary_op = (
        ((S, S, S), (S, S, S),),
        ((S, S, S), (S,),),
        ((S,), (S, S, S),),
        ((S, 1, S), (S, S),),
        ((S, S), (S, S),),
        ((), (),),
        ((S, S, S), (),),
        ((), (S, S, S),),
    )
    inputs = list((SampleInput(make_tensor(input_tensor, device, dtype,
                                           low=None, high=None,
                                           requires_grad=requires_grad),
                               args=(make_tensor(other_tensor, device, dtype,
                                                 low=None, high=None,
                                                 requires_grad=requires_grad),),))
                  for input_tensor, other_tensor in args_for_binary_op)
    return inputs
