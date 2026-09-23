def cross_product_configs(**configs):
    """
    Given configs from users, we want to generate different combinations of
    those configs
    For example, given M = ((1, 2), N = (4, 5)),
    we will generate (({'M': 1}, {'N' : 4}),
                      ({'M': 1}, {'N' : 5}),
                      ({'M': 2}, {'N' : 4}),
                      ({'M': 2}, {'N' : 5}))
    """
    _validate(configs)
    configs_attrs_list = []
    for key, values in configs.items():
        tmp_results = [{key : value} for value in values]
        configs_attrs_list.append(tmp_results)

    # TODO(mingzhe0908) remove the conversion to list.
    # itertools.product produces an iterator that produces element on the fly
    # while converting to a list produces everything at the same time.
    generated_configs = list(itertools.product(*configs_attrs_list))
    return generated_configs
