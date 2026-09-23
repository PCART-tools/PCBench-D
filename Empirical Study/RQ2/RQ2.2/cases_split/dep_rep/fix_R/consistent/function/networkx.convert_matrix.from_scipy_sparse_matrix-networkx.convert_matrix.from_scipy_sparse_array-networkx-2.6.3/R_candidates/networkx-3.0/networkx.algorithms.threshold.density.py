def density(creation_sequence):
    """
    Return the density of the graph with this creation_sequence.
    The density is the fraction of possible edges present.
    """
    N = len(creation_sequence)
    two_size = sum(degree_sequence(creation_sequence))
    two_possible = N * (N - 1)
    den = two_size / two_possible
    return den
