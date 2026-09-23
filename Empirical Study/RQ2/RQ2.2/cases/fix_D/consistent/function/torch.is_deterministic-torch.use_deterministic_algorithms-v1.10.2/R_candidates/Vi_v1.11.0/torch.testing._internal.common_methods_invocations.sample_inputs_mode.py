def sample_inputs_mode(op_info, device, dtype, requires_grad, **kwargs):
    inputs = []
    args = (
        ((S, S, S), (),),
        ((S, S, S), (1, ),),
        ((S, S, S), (1, True, ),),
        ((), (),),
        ((), (0,),),
        ((), (0, True,),),
    )
    inputs = list((SampleInput(make_tensor(input_tensor, device, dtype,
                                           low=None, high=None,
                                           requires_grad=requires_grad),
                               args=args,))
                  for input_tensor, args in args)
    return inputs
