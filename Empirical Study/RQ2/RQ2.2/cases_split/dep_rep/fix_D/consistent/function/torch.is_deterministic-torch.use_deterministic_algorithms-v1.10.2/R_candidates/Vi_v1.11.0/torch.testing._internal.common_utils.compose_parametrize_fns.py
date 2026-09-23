def compose_parametrize_fns(old_parametrize_fn, new_parametrize_fn):
    """
    Returns a parametrize_fn that parametrizes over the product of the parameters handled
    by the given parametrize_fns. Each given parametrize_fn should each have the signature
    f(test, generic_cls, device_cls).

    The test names will be a combination of the names produced by the parametrize_fns in
    "<new_name>_<old_name>" order. This order is done to match intuition for constructed names
    when composing multiple decorators; the names will be built in top to bottom order when stacking
    parametrization decorators.

    Args:
        old_parametrize_fn (callable) - First parametrize_fn to compose.
        new_parametrize_fn (callable) - Second parametrize_fn to compose.
    """

    def composite_fn(test, generic_cls, device_cls,
                     old_parametrize_fn=old_parametrize_fn,
                     new_parametrize_fn=new_parametrize_fn):
        old_tests = [(test, test_name, param_kwargs) for (test, test_name, param_kwargs) in
                     old_parametrize_fn(test, generic_cls, device_cls)]
        for (old_test, old_test_name, old_param_kwargs) in old_tests:
            for (new_test, new_test_name, new_param_kwargs) in \
                    new_parametrize_fn(old_test, generic_cls, device_cls):
                redundant_params = set(old_param_kwargs.keys()).intersection(new_param_kwargs.keys())
                if redundant_params:
                    raise RuntimeError('Parametrization over the same parameter by multiple parametrization '
                                       'decorators is not supported. For test "{}", the following parameters '
                                       'are handled multiple times: {}'.format(
                                           test.__name__, redundant_params))
                full_param_kwargs = {**old_param_kwargs, **new_param_kwargs}
                merged_test_name = '{}{}{}'.format(new_test_name,
                                                   '_' if old_test_name != '' and new_test_name != '' else '',
                                                   old_test_name)
                yield (new_test, merged_test_name, full_param_kwargs)

    return composite_fn
