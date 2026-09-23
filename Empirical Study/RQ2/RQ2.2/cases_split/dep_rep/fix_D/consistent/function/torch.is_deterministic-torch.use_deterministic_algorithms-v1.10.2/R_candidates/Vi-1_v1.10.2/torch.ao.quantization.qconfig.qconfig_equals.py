def qconfig_equals(q1: QConfigAny, q2: QConfigAny):
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
            return partial_equals(q1.activation.p, q2.activation.p) and partial_equals(q1.weight.p, q2.weight.p)
        except AttributeError:
            return q1 == q2
