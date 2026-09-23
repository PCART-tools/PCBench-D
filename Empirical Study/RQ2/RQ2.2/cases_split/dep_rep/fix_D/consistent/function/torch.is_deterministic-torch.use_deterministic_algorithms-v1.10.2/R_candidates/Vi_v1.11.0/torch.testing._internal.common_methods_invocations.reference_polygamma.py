def reference_polygamma(x, n):
    # WEIRD `scipy.special.polygamma` behavior
    # >>> scipy.special.polygamma(0, np.array(501, dtype=np.float32)).dtype
    # dtype('float64')
    # >>> scipy.special.polygamma(0, np.array([501], dtype=np.float32)).dtype
    # dtype('float32')
    #
    # Thus we cast output to the default torch dtype.
    np_dtype = torch_to_numpy_dtype_dict[torch.get_default_dtype()]
    return scipy.special.polygamma(n, x).astype(np_dtype)
