def double_flatten_states(states):
    # XXX: Can probably write this in a nicer way
    states = flatten_states([flatten_states(inner) for inner in states])
    return [hidden.view([-1] + list(hidden.shape[2:])) for hidden in states]
