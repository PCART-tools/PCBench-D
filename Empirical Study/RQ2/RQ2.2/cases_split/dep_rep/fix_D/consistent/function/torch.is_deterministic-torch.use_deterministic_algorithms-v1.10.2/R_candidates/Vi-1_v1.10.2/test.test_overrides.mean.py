@implements_diagonal(torch.mean)
def mean(mat):
    return float(mat._i) / mat._N
