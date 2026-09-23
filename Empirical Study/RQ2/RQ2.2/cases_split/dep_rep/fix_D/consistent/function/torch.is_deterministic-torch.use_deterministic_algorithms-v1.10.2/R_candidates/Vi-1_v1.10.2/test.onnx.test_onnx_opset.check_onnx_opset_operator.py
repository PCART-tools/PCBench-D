def check_onnx_opset_operator(model, ops, opset_version=_export_onnx_opset_version):
    # check_onnx_components
    assert model.ir_version == ir_version and \
        model.producer_name == producer_name and \
        model.producer_version == producer_version and \
        model.opset_import[0].version == opset_version

    # check the schema with the onnx checker
    onnx.checker.check_model(model)

    # check target type and attributes
    graph = model.graph
    # ops should contain an object for each node
    # in graph.node, in the right order.
    # At least the op_name should be specified,
    # but the op's attributes can optionally be
    # specified as well
    assert len(ops) == len(graph.node)
    for i in range(0, len(ops)):
        assert graph.node[i].op_type == ops[i]["op_name"]
        if "attributes" in ops[i] :
            attributes = ops[i]["attributes"]
            assert len(attributes) == len(graph.node[i].attribute)
            for j in range(0, len(attributes)):
                for attribute_field in attributes[j].keys():
                    assert attributes[j][attribute_field] == getattr(graph.node[i].attribute[j], attribute_field)
