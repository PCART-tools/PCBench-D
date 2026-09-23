def _findall(text, substr):
    # Also finds overlaps
    sites = []
    i = 0
    while True:
        i = text.find(substr, i)
        if i == -1:
            break
        sites.append(i)
        i += 1
    return sites
