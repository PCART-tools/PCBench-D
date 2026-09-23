def _cpu_tag(obj):
    if type(obj).__module__ == 'torch':
        return 'cpu'
