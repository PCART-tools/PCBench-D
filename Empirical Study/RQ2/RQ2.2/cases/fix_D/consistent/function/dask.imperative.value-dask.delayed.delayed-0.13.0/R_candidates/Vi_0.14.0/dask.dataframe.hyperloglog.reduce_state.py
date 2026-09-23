def reduce_state(Ms, b):
    m = 1 << b

    # We concatenated all of the states, now we need to get the max
    # value for each j in both
    Ms = Ms.reshape((len(Ms) // m), m)
    return Ms.max(axis=0)
