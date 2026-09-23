def setup_rnn_tests():
    layers_opts = [
        (1, "unilayer"),
        (3, "trilayer")
    ]
    bidirectional_opts = [
        (False, "forward"),
        (True, "bidirectional")
    ]
    initial_state_opts = [
        (True, "with_initial_state"),
        (False, "no_initial_state")
    ]
    variable_length_opts = [
        (0, "without_sequence_lengths"),
        (1, "with_variable_length_sequences"),
        (2, "with_batch_first_sequence_lengths")
    ]
    dropout_opts = [
        (0.2, "with_dropout"),
        (0.0, "without_dropout")
    ]
    test_count = 0
    for (layer, bidirectional, initial_state, variable_length, dropout) in \
        itertools.product(
            layers_opts,
            bidirectional_opts,
            initial_state_opts,
            variable_length_opts,
            dropout_opts,
    ):

        for base, name, extra_kwargs in (
                ("elman", "elman_relu", {"nonlinearity": u"relu"}),
                ("elman", "elman_tanh", {"nonlinearity": u"tanh"}),
                ("lstm", "lstm", {}),
                ("gru", "gru", {})
        ):
            make_test(name, base, layer, bidirectional, initial_state,
                      variable_length, dropout,
                      **extra_kwargs)
            test_count += 1

    # sanity check that a representative example does exist
    TestCaffe2Backend_opset9.test_gru_trilayer_forward_with_initial_state_without_sequence_lengths_with_dropout

    # make sure no one accidentally disables all the tests without
    # noticing
    assert test_count == 192, test_count
