def sparse_lengths_tensor(**kwargs):
    return sparse_segmented_tensor(segment_generator=lengths, **kwargs)
