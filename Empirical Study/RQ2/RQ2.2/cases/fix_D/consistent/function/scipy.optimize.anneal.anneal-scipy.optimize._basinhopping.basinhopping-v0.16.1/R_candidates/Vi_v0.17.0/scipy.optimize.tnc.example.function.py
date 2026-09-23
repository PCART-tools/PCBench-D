def function(x):
    f = pow(x[0],2.0)+pow(abs(x[1]),3.0)
    g = [0,0]
    g[0] = 2.0*x[0]
    g[1] = 3.0*pow(abs(x[1]),2.0)
    if x[1] < 0:
        g[1] = -g[1]
    return f, g
