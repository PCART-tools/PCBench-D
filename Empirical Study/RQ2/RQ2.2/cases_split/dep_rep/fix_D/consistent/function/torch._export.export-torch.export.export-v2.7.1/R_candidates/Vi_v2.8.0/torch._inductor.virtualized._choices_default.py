def _choices_default():
    """
    Lazy init the global choices handler

    We virtualize InductorChoices to allow changing inductor heuristics from out of tree.
    """
    from torch._inductor.choices import InductorChoices

    rv = InductorChoices()
    setattr(threadlocal, _choices._key, rv)
    return rv
