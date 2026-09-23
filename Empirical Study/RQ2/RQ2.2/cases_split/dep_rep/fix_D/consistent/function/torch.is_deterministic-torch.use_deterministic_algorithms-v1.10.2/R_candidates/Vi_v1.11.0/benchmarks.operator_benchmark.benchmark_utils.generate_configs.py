def generate_configs(**configs):
    """
    Given configs from users, we want to generate different combinations of
    those configs
    For example, given M = ((1, 2), N = (4, 5)) and sample_func being cross_product,
    we will generate (({'M': 1}, {'N' : 4}),
                      ({'M': 1}, {'N' : 5}),
                      ({'M': 2}, {'N' : 4}),
                      ({'M': 2}, {'N' : 5}))
    """
    assert 'sample_func' in configs, "Missing sample_func to generat configs"
    result = []
    for key, values in configs.items():
        if key == 'sample_func':
            continue
        tmp_result = []
        for value in values:
            tmp_result.append({key : value})
        result.append(tmp_result)

    results = configs['sample_func'](*result)
    return results
