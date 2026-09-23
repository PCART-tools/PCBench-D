def no_observer_set() -> Set[Any]:
    r"""These modules cannot have observers inserted by default."""
    no_observers = set([
        nn.quantizable.LSTM,
        nn.quantizable.MultiheadAttention
    ])
    return no_observers
