def _generate_training_net_only(model, include_tags=None):
    train_net = core.Net('train_net')
    train_init_net = model.create_init_net('train_init_net')

    for layer in _filter_layers(model.layers, include_tags):
        if Tags.EXCLUDE_FROM_TRAIN not in layer.tags:
            layer.add_operators(train_net, train_init_net)

    input_schema = model.input_feature_schema + model.trainer_extra_schema
    train_net.set_input_record(input_schema)
    output_schema = shrink_output_schema(
        train_net, model.output_schema + model.metrics_schema
    )
    train_net.set_output_record(output_schema)
    return train_init_net, train_net
