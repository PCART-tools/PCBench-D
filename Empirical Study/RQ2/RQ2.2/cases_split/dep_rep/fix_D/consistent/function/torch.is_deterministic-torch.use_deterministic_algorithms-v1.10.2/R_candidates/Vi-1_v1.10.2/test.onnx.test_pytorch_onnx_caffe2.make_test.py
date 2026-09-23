def make_test(name, base, layer, bidirectional, initial_state,
              variable_length, dropout,
              **extra_kwargs):
    test_name = str("_".join([
        "test", name, layer[1],
        bidirectional[1], initial_state[1],
        variable_length[1], dropout[1]
    ]))

    @unittest.skip("Disabled due to onnx optimizer deprecation")
    @skipIfUnsupportedOpsetVersion([10])
    @skipIfUnsupportedMinOpsetVersion(8)
    def f(self):
        self._dispatch_rnn_test(
            base,
            layers=layer[0],
            bidirectional=bidirectional[0],
            initial_state=initial_state[0],
            packed_sequence=variable_length[0],
            dropout=dropout[0],
            **extra_kwargs)

    f.__name__ = test_name
    setattr(TestCaffe2Backend_opset9, f.__name__, f)
