def equalize(model, paired_modules_list, threshold=1e-4, inplace=True):
    ''' Given a list of adjacent modules within a model, equalization will
    be applied between each pair, this will repeated until convergence is achieved

    Keeps a copy of the changing modules from the previous iteration, if the copies
    are not that different than the current modules (determined by converged_test),
    then the modules have converged enough that further equalizing is not necessary

    Implementation of this referced section 4.1 of this paper https://arxiv.org/pdf/1906.04721.pdf

    Args:
        model: a model (nn.module) that equalization is to be applied on
        paired_modules_list: a list of lists where each sublist is a pair of two
            submodules found in the model, for each pair the two submodules generally
            have to be adjacent in the model to get expected/reasonable results
        threshold: a number used by the converged function to determine what degree
            similarity between models is necessary for them to be called equivalent
        inplace: determines if function is inplace or not
    '''
    if not inplace:
        model = copy.deepcopy(model)

    name_to_module : Dict[str, torch.nn.Module] = {}
    previous_name_to_module: Dict[str, Any] = {}
    name_set = {name for pair in paired_modules_list for name in pair}

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
