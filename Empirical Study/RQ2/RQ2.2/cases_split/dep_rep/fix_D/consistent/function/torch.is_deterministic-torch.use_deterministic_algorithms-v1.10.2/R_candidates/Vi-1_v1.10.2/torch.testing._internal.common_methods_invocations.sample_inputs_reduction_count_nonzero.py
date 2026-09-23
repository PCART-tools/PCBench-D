def sample_inputs_reduction_count_nonzero(*args, **kwargs):
    """Sample inputs for count_nonzero"""
    samples: List[SampleInput] = sample_inputs_reduction(*args, **kwargs)
    # count_nonzero does not support keepdim yet
    for sample in samples:
        sample.kwargs.pop('keepdim', None)
    return samples
