def generate_predict_net(model, include_tags=None):
    predict_net = core.Net('predict_net')

    for layer in _filter_layers(model.layers, include_tags):
        if Tags.EXCLUDE_FROM_PREDICTION not in layer.tags:
            layer.add_operators(
                predict_net, context=InstantiationContext.PREDICTION)

    predict_net.set_input_record(model.input_feature_schema.clone())
    output_schema = shrink_output_schema(
        predict_net, model.output_schema.clone()
    )
    predict_net.set_output_record(output_schema)
    return predict_net
