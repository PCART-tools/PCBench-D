def make_test(name, base, layer, bidirectional, initial_state,
              variable_length, dropout, script_test_min_opset_version,
              **extra_kwargs):
    test_name = str("_".join([
        "test", name, layer[1],
        bidirectional[1], initial_state[1],
        variable_length[1], dropout[1]
    ]))

    # Cannot export with older opsets because of "ConstantFill" op
    # ConstantFill was a temp op removed at opset 8. This is no longer supported by onnxruntime
    # There are still some issues prevent us from enabling script test for these scenarios:
    # test_gru_*:
    #   Operator aten::as_tensor is not supported by exporter yet.
    #       - https://msdata.visualstudio.com/Vienna/_workitems/edit/1055382
    #   Operator aten::_pack_padded_sequence is not supported by exporter yet.
    #       - https://msdata.visualstudio.com/Vienna/_workitems/edit/1055384
    @disableScriptTest()
    @skipIfUnsupportedMinOpsetVersion(9)
    def f(self):
        self.is_script_test_enabled = self.opset_version >= script_test_min_opset_version
        self._dispatch_rnn_test(
            base,
            layers=layer[0],
            bidirectional=bidirectional[0],
            initial_state=initial_state[0],
            packed_sequence=variable_length[0],
            dropout=dropout[0],
            **extra_kwargs)

    f.__name__ = test_name
    setattr(TestONNXRuntime, f.__name__, f)
