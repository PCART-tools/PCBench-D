def kldivloss_with_log_target_no_reduce_test():
    i = torch.rand(10, 10).log()
    return dict(
        fullname='KLDivLoss_with_log_target_no_reduce',
        constructor=wrap_functional(
            lambda t: F.kl_div(i.type_as(t), t, reduction='none', log_target=True)),
        cpp_function_call='F::kl_div(i.to(t.options()), t, F::KLDivFuncOptions().reduction(torch::kNone).log_target(true))',
        input_fn=lambda: torch.rand(10, 10),
        cpp_var_map={'i': i, 't': '_get_input()'},
        reference_fn=lambda t, *_:
            loss_reference_fns['KLDivLoss_log_target'](i.type_as(t), t, reduction='none'),
        supports_forward_ad=True,
        pickle=False)
