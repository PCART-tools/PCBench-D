def assertEqual(tensor, expected, threshold=0.001):
    if isinstance(tensor, list) or isinstance(tensor, tuple):
        for t, e in zip(tensor, expected):
            assertEqual(t, e)
    else:
        if (tensor - expected).abs().max() > threshold:
            barf()
