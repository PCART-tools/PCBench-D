def adm(a, criterion):
    """\nReturns rows from the passed list of lists that meet the criteria in
the passed criterion expression (a string).

Format:  adm (a,criterion)   where criterion is like 'x[2]==37'\n"""

    lines = eval('filter(lambda x: '+criterion+',a)')
    try:
        lines = np.array(lines)
    except:
        lines = np.array(lines,'O')
    return lines
