def _apply_func(x,g,func):
    # g is list of indices into x
    #  separating x into different groups
    #  func should be applied over the groups
    g = unique(r_[0,g,len(x)])
    output = []
    for k in range(len(g)-1):
        output.append(func(x[g[k]:g[k+1]]))
    return asarray(output)
