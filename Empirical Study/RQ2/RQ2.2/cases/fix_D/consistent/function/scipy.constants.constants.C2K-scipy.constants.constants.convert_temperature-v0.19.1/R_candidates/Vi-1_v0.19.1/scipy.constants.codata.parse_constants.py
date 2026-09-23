def parse_constants(d):
    constants = {}
    for line in d.split('\n'):
        name = line[:55].rstrip()
        val = line[55:77].replace(' ', '').replace('...', '')
        val = float(val)
        uncert = line[77:99].replace(' ', '').replace('(exact)', '0')
        uncert = float(uncert)
        units = line[99:].rstrip()
        constants[name] = (val, units, uncert)
    return constants
