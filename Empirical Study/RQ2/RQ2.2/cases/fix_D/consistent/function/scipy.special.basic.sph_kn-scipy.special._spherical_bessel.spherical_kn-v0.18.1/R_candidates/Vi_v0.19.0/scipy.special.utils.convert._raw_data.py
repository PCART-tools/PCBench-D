def _raw_data(line):
    items = line.split(',')
    l = []
    for item in items:
        m = ITEM_REGEX.search(item)
        if m:
            q = m.group(0)
            l.append(q)
    return l
