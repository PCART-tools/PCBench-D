def sigmoid_cross_entropy_with_logits_grad(x, z):
    return z - sigmoid(x)
