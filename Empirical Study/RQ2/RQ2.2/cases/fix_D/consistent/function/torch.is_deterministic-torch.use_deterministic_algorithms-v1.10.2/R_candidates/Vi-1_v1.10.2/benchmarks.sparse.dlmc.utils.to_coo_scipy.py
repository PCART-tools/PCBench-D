def to_coo_scipy(x):
    indices_1 = x._indices().numpy()
    values_1 = x._values().numpy()
    return sparse.coo_matrix((values_1, (indices_1[0], indices_1[1])),
                             shape=x.shape)
