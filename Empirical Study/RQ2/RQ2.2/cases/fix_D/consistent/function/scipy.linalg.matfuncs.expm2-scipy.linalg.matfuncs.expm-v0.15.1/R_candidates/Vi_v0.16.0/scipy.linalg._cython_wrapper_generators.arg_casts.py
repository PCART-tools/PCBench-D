def arg_casts(arg):
    if arg in ['npy_complex64', 'npy_complex128', '_cselect1', '_cselect2',
               '_dselect2', '_dselect3', '_sselect2', '_sselect3',
               '_zselect1', '_zselect2']:
        return '<{}*>'.format(arg)
    return ''
