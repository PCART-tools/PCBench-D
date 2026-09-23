def check_sample_meanvar_(distfn, arg, m, v, sm, sv, sn, msg):
    # this did not work, skipped silently by nose
    if not np.isinf(m):
        check_sample_mean(sm, sv, sn, m)
    if not np.isinf(v):
        check_sample_var(sv, sn, v)
