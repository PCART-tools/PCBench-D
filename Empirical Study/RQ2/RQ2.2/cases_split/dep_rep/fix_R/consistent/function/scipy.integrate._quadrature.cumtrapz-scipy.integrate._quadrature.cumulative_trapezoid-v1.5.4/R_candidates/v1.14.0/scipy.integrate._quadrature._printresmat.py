def _printresmat(function, interval, resmat):
    # Print the Romberg result matrix.
    i = j = 0
    print('Romberg integration of', repr(function), end=' ')
    print('from', interval)
    print('')
    print('%6s %9s %9s' % ('Steps', 'StepSize', 'Results'))
    for i in range(len(resmat)):
        print('%6d %9f' % (2**i, (interval[1]-interval[0])/(2.**i)), end=' ')
        for j in range(i+1):
            print('%9f' % (resmat[i][j]), end=' ')
        print('')
    print('')
    print('The final result is', resmat[i][j], end=' ')
    print('after', 2**(len(resmat)-1)+1, 'function evaluations.')
