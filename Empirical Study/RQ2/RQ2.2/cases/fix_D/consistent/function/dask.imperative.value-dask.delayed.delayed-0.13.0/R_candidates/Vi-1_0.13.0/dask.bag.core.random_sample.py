def random_sample(x, state_data, prob):
    """Filter elements of `x` by a probability `prob`

    Parameters
    ----------
    x : iterable
    state_data : tuple
        A tuple that can be passed to ``random.Random``.
    prob : float
        A float between 0 and 1, representing the probability that each
        element will be yielded.
    """
    random_state = Random(state_data)
    for i in x:
        if random_state.random() < prob:
            yield i
