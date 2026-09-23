@_silence_fp_errors
def check_sample_meanvar_(distfn, arg, m, v, sm, sv, sn, msg):
    # this did not work, skipped silently by nose
    # check_sample_meanvar, sm, m, msg + 'sample mean test'
    # check_sample_meanvar, sv, v, msg + 'sample var test'
    if not np.isinf(m):
        check_sample_mean(sm, sv, sn, m)
    if not np.isinf(v):
        check_sample_var(sv, sn, v)
