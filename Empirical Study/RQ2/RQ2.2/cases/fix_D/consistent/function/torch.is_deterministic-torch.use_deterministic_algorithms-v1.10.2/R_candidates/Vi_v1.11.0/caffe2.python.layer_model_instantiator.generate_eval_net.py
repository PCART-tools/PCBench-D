def generate_eval_net(model, include_tags=None):
    eval_net = core.Net('eval_net')

    for layer in _filter_layers(model.layers, include_tags):
        if Tags.EXCLUDE_FROM_EVAL not in layer.tags:
            layer.add_operators(eval_net, context=InstantiationContext.EVAL)

    input_schema = model.input_feature_schema + model.trainer_extra_schema
    eval_net.set_input_record(input_schema)
    output_schema = shrink_output_schema(
        eval_net, model.output_schema + model.metrics_schema
    )
    eval_net.set_output_record(output_schema)
    return eval_net
