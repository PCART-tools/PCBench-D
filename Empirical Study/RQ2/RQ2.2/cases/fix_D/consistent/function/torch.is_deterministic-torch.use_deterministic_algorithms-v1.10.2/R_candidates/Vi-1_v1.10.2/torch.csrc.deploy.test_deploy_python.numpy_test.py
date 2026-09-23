def numpy_test(x):
    import numpy as np
    xs = [np.array([x, x]), np.array([x, x])]
    for i in range(10):
        xs.append(xs[-1] + xs[-2])
    return int(xs[-1][0])
