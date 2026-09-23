def tensors(n, min_dim=1, max_dim=4, dtype=np.float32, elements=None, **kwargs):
    dims_ = st.lists(dims(**kwargs), min_size=min_dim, max_size=max_dim)
    return dims_.flatmap(
        lambda dims: st.lists(
            arrays(dims, dtype, elements),
            min_size=n,
            max_size=n))
