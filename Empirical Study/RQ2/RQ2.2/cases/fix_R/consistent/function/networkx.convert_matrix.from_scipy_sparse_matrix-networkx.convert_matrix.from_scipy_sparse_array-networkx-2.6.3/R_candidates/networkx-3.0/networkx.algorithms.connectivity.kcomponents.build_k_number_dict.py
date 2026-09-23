def build_k_number_dict(kcomps):
    result = {}
    for k, comps in sorted(kcomps.items(), key=itemgetter(0)):
        for comp in comps:
            for node in comp:
                result[node] = k
    return result
