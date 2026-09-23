class TimerMac(_macosx.Timer, TimerBase):
    '''
    Subclass of :class:`backend_bases.TimerBase` that uses CoreFoundation
    run loops for timer events.

    Attributes
    ----------
    interval : int
        The time between timer events in milliseconds. Default is 1000 ms.
    single_shot : bool
        Boolean flag indicating whether this timer should operate as single
        shot (run once and then stop). Defaults to False.
    callbacks : list
        Stores list of (func, args) tuples that will be called upon timer
        events. This list can be manipulated directly, or the functions
        `add_callback` and `remove_callback` can be used.

    '''
