def max_over_ndim(input, axis_list, keepdim=False):
    ''' Applies 'torch.max' over the given axises
    '''
    axis_list.sort(reverse=True)
    for axis in axis_list:
        input, _ = input.max(axis, keepdim)
    return input
