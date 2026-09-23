def dummy_fetcher_rnn(fetcher_id, batch_size):
    # Hardcoding some input blobs
    T = 20
    N = batch_size
    D = 33
    data = np.random.rand(T, N, D)
    label = np.random.randint(N, size=(T, N))
    seq_lengths = np.random.randint(N, size=(N))
    return [data, label, seq_lengths]
