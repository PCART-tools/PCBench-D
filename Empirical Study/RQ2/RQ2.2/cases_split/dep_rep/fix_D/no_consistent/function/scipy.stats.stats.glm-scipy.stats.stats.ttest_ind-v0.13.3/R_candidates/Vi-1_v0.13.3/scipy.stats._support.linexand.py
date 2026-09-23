def linexand(a, columnlist, valuelist):
    """Returns the rows of an array where col (from columnlist) = val
    (from valuelist).  One value is required for each column in columnlist.

    Returns: the rows of a where columnlist[i]=valuelist[i] for ALL i\n"""

    a = asarray(a)
    if type(columnlist) not in [ListType,TupleType,np.ndarray]:
        columnlist = [columnlist]
    if type(valuelist) not in [ListType,TupleType,np.ndarray]:
        valuelist = [valuelist]
    criterion = ''
    for i in range(len(columnlist)):
        if type(valuelist[i]) == StringType:
            critval = '\'' + valuelist[i] + '\''
        else:
            critval = str(valuelist[i])
        criterion = criterion + ' x['+str(columnlist[i])+']=='+critval+' and'
    criterion = criterion[0:-3]         # remove the "and" after the last crit
    return adm(a,criterion)
