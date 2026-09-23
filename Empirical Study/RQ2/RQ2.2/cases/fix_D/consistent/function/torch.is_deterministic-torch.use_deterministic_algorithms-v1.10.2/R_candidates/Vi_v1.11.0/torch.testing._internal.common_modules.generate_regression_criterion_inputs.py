def generate_regression_criterion_inputs(make_input):
    return [
        ModuleInput(
            constructor_input=FunctionInput(reduction=reduction),
            forward_input=FunctionInput(make_input(shape=(4, )), make_input(shape=4,)),
            reference_fn=partial(no_batch_dim_reference_fn, is_criterion=True),
            desc='no_batch_dim_{}'.format(reduction)
        ) for reduction in ['none', 'mean', 'sum']]
