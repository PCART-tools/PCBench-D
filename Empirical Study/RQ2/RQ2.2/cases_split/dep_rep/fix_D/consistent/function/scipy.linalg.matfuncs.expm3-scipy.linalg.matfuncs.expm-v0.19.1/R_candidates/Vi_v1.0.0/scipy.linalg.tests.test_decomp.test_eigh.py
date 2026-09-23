def test_eigh():
    DIM = 6
    v = {'dim': (DIM,),
         'dtype': ('f','d','F','D'),
         'overwrite': (True, False),
         'lower': (True, False),
         'turbo': (True, False),
         'eigvals': (None, (2, DIM-2))}

    for dim in v['dim']:
        for typ in v['dtype']:
            for overwrite in v['overwrite']:
                for turbo in v['turbo']:
                    for eigenvalues in v['eigvals']:
                        for lower in v['lower']:
                            eigenhproblem_standard(
                                   'ordinary',
                                   dim, typ, overwrite, lower,
                                   turbo, eigenvalues)
                            eigenhproblem_general(
                                   'general ',
                                   dim, typ, overwrite, lower,
                                   turbo, eigenvalues)
