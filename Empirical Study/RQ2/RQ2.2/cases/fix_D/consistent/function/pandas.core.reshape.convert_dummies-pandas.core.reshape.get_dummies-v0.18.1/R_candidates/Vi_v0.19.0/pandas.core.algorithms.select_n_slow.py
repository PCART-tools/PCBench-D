def select_n_slow(dropped, n, keep, method):
    reverse_it = (keep == 'last' or method == 'nlargest')
    ascending = method == 'nsmallest'
    slc = np.s_[::-1] if reverse_it else np.s_[:]
    return dropped[slc].sort_values(ascending=ascending).head(n)
