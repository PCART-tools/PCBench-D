def _ValidateParams(params):
    set_params = set(params)
    if len(params) > len(set_params):
        dupes = []
        sp = sorted(params)
        for j, p in enumerate(sp):
            if j > 0 and sp[j - 1] == p:
                dupes.append(p)

        assert len(params) == len(set_params), \
            "Duplicate entries in params: {}".format(dupes)
