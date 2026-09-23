def dummy_fetcher(fetcher_id, batch_size):
    # Create random amount of values
    n = np.random.randint(64) + 1
    data = np.zeros((n, 3))
    labels = []
    for j in range(n):
        data[j, :] *= (j + fetcher_id)
        labels.append(data[j, 0])

    return [np.array(data), np.array(labels)]
