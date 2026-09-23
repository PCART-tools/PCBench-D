def sparse_lengths_mean_ref(D, I, L):
    return sparse_lengths_sum_ref(D, I, L, normalize_by_lengths=True)
