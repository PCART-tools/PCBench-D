def get_mat(n):
    data = np.arange(n)
    data = np.add.outer(data, data)
    return data
