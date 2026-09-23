def generate_training_nets(model, include_tags=None):
    train_init_net, train_net = _generate_training_net_only(model, include_tags)

    model.apply_regularizers_on_loss(train_net, train_init_net)
    if not model.has_loss():
        return train_init_net, train_net
    loss = model.loss
    grad_map = train_net.AddGradientOperators(loss.field_blobs())
    model.apply_post_grad_net_modifiers(train_net, train_init_net, grad_map,
                                        modify_output_record=True)
    model.apply_optimizers(train_net, train_init_net, grad_map)
    model.apply_regularizers_after_optimizer(train_net, train_init_net, grad_map)
    model.apply_final_net_modifiers(train_net, train_init_net, grad_map,
                                    modify_output_record=True)

    return train_init_net, train_net
