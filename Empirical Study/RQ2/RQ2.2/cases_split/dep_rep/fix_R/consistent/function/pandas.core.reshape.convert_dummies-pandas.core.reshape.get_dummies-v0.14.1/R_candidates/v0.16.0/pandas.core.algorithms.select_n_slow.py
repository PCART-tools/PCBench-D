def select_n_slow(dropped, n, take_last, method):
    reverse_it = take_last or method == 'nlargest'
    ascending = method == 'nsmallest'
    slc = np.s_[::-1] if reverse_it else np.s_[:]
    return dropped[slc].order(ascending=ascending).head(n)
