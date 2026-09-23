def random_sample_configs(**configs):
    """
    This function randomly sample <total_samples> values from the given inputs based on
    their weights.
    Here is an example showing what are the expected inputs and outpus from this function:
    M = [1, 2],
    N = [4, 5],
    K = [7, 8],
    probs = attr_probs(
        M = [0.7, 0.2],
        N = [0.5, 0.2],
        K = [0.6, 0.2],
    ),
    total_samples=10,
    this function will generate
    [
        [{'K': 7}, {'M': 1}, {'N': 4}],
        [{'K': 7}, {'M': 2}, {'N': 5}],
        [{'K': 8}, {'M': 2}, {'N': 4}],
        ...
    ]
    Note:
    The probs is optional. Without them, it implies everything is 1. The probs doesn't
    have to reflect the actual normalized probability, the implementation will
    normalize it.
    TODO (mingzhe09088):
    (1):  a lambda that accepts or rejects a config as a sample. For example: for matmul
    with M, N, and K, this function could get rid of (M * N * K > 1e8) to filter out
    very slow benchmarks.
    (2): Make sure each sample is unique. If the number of samples are larger than the
    total combinations, just return the cross product. Otherwise, if the number of samples
    is close to the number of cross-products, it is numerical safer to generate the list
    that you don't want, and remove them.
    """
    if "probs" not in configs:
        raise ValueError("probs is missing. Consider adding probs or"
                         "using other config functions")

    configs_attrs_list = []
    randomsample = RandomSample(configs)
    for i in range(configs["total_samples"]):
        tmp_attr_list = randomsample.get_one_set_of_inputs()
        tmp_attr_list.append({"tags" : '_'.join(configs["tags"])})
        configs_attrs_list.append(tmp_attr_list)
    return configs_attrs_list
