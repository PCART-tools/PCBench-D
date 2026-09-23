def get_input_tensors():
    height = np.random.randint(1, 10)
    width = np.random.randint(1, 10)
    dtype = np.float32
    input_tensor = hu.arrays(
        dims=[height, width],
        dtype=dtype,
        elements=st.integers(min_value=0, max_value=100),
    )

    return input_tensor
