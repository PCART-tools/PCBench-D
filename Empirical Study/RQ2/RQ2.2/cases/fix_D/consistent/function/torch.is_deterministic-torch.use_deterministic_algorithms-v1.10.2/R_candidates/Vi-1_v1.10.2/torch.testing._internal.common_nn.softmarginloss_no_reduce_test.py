def softmarginloss_no_reduce_test():
    t = torch.randn(5, 5)
    return dict(
        fullname='SoftMarginLoss_no_reduce',
        constructor=wrap_functional(
            lambda i: F.soft_margin_loss(i, t.type_as(i), reduction='none')),
        cpp_function_call='''F::soft_margin_loss(
            i, t.to(i.options()), F::SoftMarginLossFuncOptions().reduction(torch::kNone))''',
        input_fn=lambda: torch.randn(5, 5),
        cpp_var_map={'i': '_get_input()', 't': t},
        reference_fn=lambda i, *_:
            loss_reference_fns['SoftMarginLoss'](i, t.type_as(i), reduction='none'),
        pickle=False)
