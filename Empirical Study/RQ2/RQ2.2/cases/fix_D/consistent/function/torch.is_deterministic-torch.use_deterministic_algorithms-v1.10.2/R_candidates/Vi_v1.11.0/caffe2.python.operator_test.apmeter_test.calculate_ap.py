def calculate_ap(predictions, labels):
    N, D = predictions.shape
    ap = np.zeros(D)
    num_range = np.arange((N), dtype=np.float32) + 1
    for k in range(D):
        scores = predictions[:N, k]
        label = labels[:N, k]
        sortind = np.argsort(-scores, kind='mergesort')
        truth = label[sortind]
        precision = np.cumsum(truth) / num_range
        ap[k] = precision[truth.astype(np.bool)].sum() / max(1, truth.sum())
    return ap
