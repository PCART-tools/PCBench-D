def tensor(min_dim=1,
           max_dim=4,
           dtype=np.float32,
           elements=None,
           unique=False,
           **kwargs):
    dims_ = st.lists(dims(**kwargs), min_size=min_dim, max_size=max_dim)
    return dims_.flatmap(
        lambda dims: arrays(dims, dtype, elements, unique=unique))
