def sigmoid_cross_entropy_with_logits_with_log_D_trick(x, z):
    return -(2 * z - 1.) * np.log(sigmoid(x))
