def make_sample_test_batch(raw_data_path, processed_data_path, device):
    """Create the test_data_loader and sample a batch from it. This batch will be used
    to measure the forward pass of the model throughout this experiment.
    """
    test_data_loader = make_test_data_loader(raw_data_path, processed_data_path)

    test_iter = iter(test_data_loader)

    test_batch = next(test_iter)

    X_test, lS_o_test, lS_i_test, _, _, _ = unpack_batch(test_batch)

    X, lS_o, lS_i = dlrm_wrap(X_test, lS_o_test, lS_i_test, device)
    batch = {"X": X, "lS_o": lS_o, "lS_i": lS_i}

    return batch
