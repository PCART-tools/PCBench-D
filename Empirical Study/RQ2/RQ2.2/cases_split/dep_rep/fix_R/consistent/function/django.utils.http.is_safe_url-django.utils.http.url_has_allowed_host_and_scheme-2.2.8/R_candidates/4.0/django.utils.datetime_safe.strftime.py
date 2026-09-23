def strftime(dt, fmt):
    if dt.year >= 1000:
        return super(type(dt), dt).strftime(fmt)
    illegal_formatting = _illegal_formatting.search(fmt)
    if illegal_formatting:
        raise TypeError('strftime of dates before 1000 does not handle ' + illegal_formatting[0])

    year = dt.year
    # For every non-leap year century, advance by
    # 6 years to get into the 28-year repeat cycle
    delta = 2000 - year
    off = 6 * (delta // 100 + delta // 400)
    year = year + off

    # Move to around the year 2000
    year = year + ((2000 - year) // 28) * 28
    timetuple = dt.timetuple()
    s1 = time.strftime(fmt, (year,) + timetuple[1:])
    sites1 = _findall(s1, str(year))

    s2 = time.strftime(fmt, (year + 28,) + timetuple[1:])
    sites2 = _findall(s2, str(year + 28))

    sites = []
    for site in sites1:
        if site in sites2:
            sites.append(site)

    s = s1
    syear = "%04d" % dt.year
    for site in sites:
        s = s[:site] + syear + s[site + 4:]
    return s
