def min_over_ndim(input, axis_list, keepdim=False):
    ''' Applies 'torch.min' over the given axises
    '''
    axis_list.sort(reverse=True)
    for axis in axis_list:
        input, _ = input.min(axis, keepdim)
    return input
