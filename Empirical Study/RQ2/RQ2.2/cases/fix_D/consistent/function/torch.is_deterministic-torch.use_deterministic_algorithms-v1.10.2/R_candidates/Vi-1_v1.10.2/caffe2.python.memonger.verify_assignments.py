def verify_assignments(assignments):
    for cur in assignments:
        for x, y in zip(cur[0:-1], cur[1:]):
            assert x[1].used < y[1].defined
