def process_fortran_name(name, funcname):
    if 'inc' in name:
        return name
    xy_exclusions = ['ladiv', 'lapy2', 'lapy3']
    if ('x' in name or 'y' in name) and funcname[1:] not in xy_exclusions:
        return name + '(n)'
    if name in dims:
        return name + dims[name]
    return name
