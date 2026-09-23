def qconfig_equals(q1: QConfigAny, q2: QConfigAny):
    """
    Returns `True` if `q1` equals `q2`, and `False` otherwise.
    """
    # functools.partial has no __eq__ operator defined so '==' defaults to 'is'
    def partial_equals(p1, p2):
        same = p1.func == p2.func
        same = same and p1.args == p2.args
        return same and p1.keywords == p2.keywords

    if q1 is None or q2 is None:
        return q1 == q2
    else:
        assert q1 is not None and q2 is not None
        try:
            # Qconfig weight and activation can be either a partial wrapper,
            # or an observer class. Special handling is required (above) for
            # comparing partial wrappers.
            if(isinstance(q1.activation, torch.ao.quantization.observer._PartialWrapper)):
                activation_same = partial_equals(q1.activation.p, q2.activation.p)
            else:
                activation_same = q1.activation == q2.activation
            if(isinstance(q1.weight, torch.ao.quantization.observer._PartialWrapper)):
                weight_same = partial_equals(q1.weight.p, q2.weight.p)
            else:
                weight_same = q1.weight == q2.weight

            return activation_same and weight_same
        except AttributeError:
            return q1 == q2
