def construct_name(fwd_bwd, test_name):
    bwd = 'backward' in fwd_bwd
    suite_name = fwd_bwd.replace('-backward', '')
    return '{suite}[{test}]:{fwd_bwd}'.format(suite=suite_name, test=test_name, fwd_bwd='bwd' if bwd else 'fwd')
