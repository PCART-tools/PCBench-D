def nonzero_numpy(g, input, _outputs=None):
    return unbind(g, nonzero(g, input), 1, _outputs=_outputs)
