def jsd(p, q):
    return [entropy(p / 2. + q / 2.) - entropy(p) / 2. - entropy(q) / 2.]
