def masked_var(am):
    m = am.mean()
    s = ma.add.reduce((am - m)**2)
    n = am.count() - 1.0
    return s / n
