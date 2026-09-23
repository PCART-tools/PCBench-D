def lengths_tensor(min_segments=None, max_segments=None, *args, **kwargs):
    gen = functools.partial(
        lengths, min_segments=min_segments, max_segments=max_segments)
    return segmented_tensor(*args, segment_generator=gen, **kwargs)
