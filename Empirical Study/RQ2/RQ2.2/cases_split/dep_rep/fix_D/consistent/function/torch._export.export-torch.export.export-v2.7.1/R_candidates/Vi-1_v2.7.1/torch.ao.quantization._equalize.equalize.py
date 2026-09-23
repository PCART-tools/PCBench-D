def equalize(model, paired_modules_list, threshold=1e-4, inplace=True):
    """Equalize modules until convergence is achieved.

    Given a list of adjacent modules within a model, equalization will
    be applied between each pair, this will repeated until convergence is achieved

    Keeps a copy of the changing modules from the previous iteration, if the copies
    are not that different than the current modules (determined by converged_test),
    then the modules have converged enough that further equalizing is not necessary

    Reference is section 4.1 of this paper https://arxiv.org/pdf/1906.04721.pdf

    Args:
        model: a model (nn.Module) that equalization is to be applied on
            paired_modules_list (List(List[nn.module || str])): a list of lists
            where each sublist is a pair of two submodules found in the model,
            for each pair the two modules have to be adjacent in the model,
            with only piece-wise-linear functions like a (P)ReLU or LeakyReLU in between
            to get expected results.
            The list can contain either modules, or names of modules in the model.
            If you pass multiple modules in the same list, they will all be equalized together.
            threshold (float): a number used by the converged function to determine what degree
            of similarity between models is necessary for them to be called equivalent
        inplace (bool): determines if function is inplace or not
    """

    paired_modules_list = process_paired_modules_list_to_name(
        model, paired_modules_list
    )

    if not inplace:
        model = copy.deepcopy(model)

    paired_modules_list = expand_groups_in_paired_modules_list(paired_modules_list)

    name_to_module: dict[str, torch.nn.Module] = {}
    previous_name_to_module: dict[str, Any] = {}
    name_set = set(chain.from_iterable(paired_modules_list))

    for name, module in model.named_modules():
        if name in name_set:
            name_to_module[name] = module
            previous_name_to_module[name] = None
    while not converged(name_to_module, previous_name_to_module, threshold):
        for pair in paired_modules_list:
            previous_name_to_module[pair[0]] = copy.deepcopy(name_to_module[pair[0]])
            previous_name_to_module[pair[1]] = copy.deepcopy(name_to_module[pair[1]])

            cross_layer_equalization(name_to_module[pair[0]], name_to_module[pair[1]])

    return model
