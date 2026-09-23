def generate_training_nets_forward_only(model, include_tags=None):
    train_init_net, train_net = _generate_training_net_only(model, include_tags)
    return train_init_net, train_net
