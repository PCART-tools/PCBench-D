def module_inputs_torch_nn_CrossEntropyLoss(module_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=torch.long, requires_grad=False)
    make_weight = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    reductions = ['sum', 'mean', 'none']
    samples = []
    # Samples below are for validating the no-batch-dim support.
    for reduction in reductions:
        samples.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction),
                        forward_input=FunctionInput(make_input(shape=(9,)), make_target(shape=(), low=0, high=9)),
                        reference_fn=partial(no_batch_dim_reference_fn, is_criterion=True))
        )
        samples.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction, weight=make_weight(shape=(9,))),
                        forward_input=FunctionInput(make_input(shape=(9,)), make_target(shape=(), low=0, high=9)),
                        reference_fn=partial(no_batch_dim_reference_fn, is_criterion=True))
        )
        samples.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction, label_smoothing=0.5),
                        forward_input=FunctionInput(make_input(shape=(9,)), make_target(shape=(), low=0, high=9)),
                        reference_fn=partial(no_batch_dim_reference_fn, is_criterion=True))
        )
        samples.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction, label_smoothing=0.5,
                                                        weight=make_weight(shape=(9,))),
                        forward_input=FunctionInput(make_input(shape=(9,)), make_target(shape=(), low=0, high=9)),
                        reference_fn=partial(no_batch_dim_reference_fn, is_criterion=True))
        )

    return samples
