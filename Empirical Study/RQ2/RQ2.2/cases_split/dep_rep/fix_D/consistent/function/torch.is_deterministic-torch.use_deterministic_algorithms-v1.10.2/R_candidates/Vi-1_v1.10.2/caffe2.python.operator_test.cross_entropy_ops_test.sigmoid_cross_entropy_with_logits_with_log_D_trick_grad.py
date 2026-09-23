def sigmoid_cross_entropy_with_logits_with_log_D_trick_grad(x, z):
    return (2 * z - 1.) * (1 - sigmoid(x))
