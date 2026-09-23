def softmax(w):
    maxes = np.amax(w, axis=-1, keepdims=True)
    e = np.exp(w - maxes)
    dist = e / np.sum(e, axis=-1, keepdims=True)
    return dist
