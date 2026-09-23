def divide_to_width(desired_chunks, max_width):
    """ Minimally divide the given chunks so as to make the largest chunk
    width less or equal than *max_width*.
    """
    chunks = []
    for c in desired_chunks:
        nb_divides = int(np.ceil(c / max_width))
        for i in range(nb_divides):
            n = c // (nb_divides - i)
            chunks.append(n)
            c -= n
        assert c == 0
    return tuple(chunks)
