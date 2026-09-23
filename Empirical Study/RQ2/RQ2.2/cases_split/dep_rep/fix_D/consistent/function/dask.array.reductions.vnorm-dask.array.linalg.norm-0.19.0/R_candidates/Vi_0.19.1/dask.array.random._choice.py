def _choice(state_data, a, size, replace, p):
    state = np.random.RandomState(state_data)
    return state.choice(a, size=size, replace=replace, p=p)
