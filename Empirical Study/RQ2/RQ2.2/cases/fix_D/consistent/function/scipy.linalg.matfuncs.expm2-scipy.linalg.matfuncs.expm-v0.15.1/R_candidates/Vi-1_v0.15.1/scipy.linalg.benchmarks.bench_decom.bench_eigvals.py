def bench_eigvals():
    numpy_eigvals = nl.eigvals
    scipy_eigvals = sl.eigvals
    print()
    print('           Finding matrix eigenvalues')
    print('      ==================================')
    print('      |    contiguous     |   non-contiguous ')
    print('----------------------------------------------')
    print(' size |  scipy  | numpy   |  scipy  | numpy ')

    for size,repeat in [(20,150),(100,7),(200,2)]:
        repeat *= 1
        print('%5s' % size, end=' ')
        sys.stdout.flush()

        a = random([size,size])

        print('| %6.2f ' % measure('scipy_eigvals(a)',repeat), end=' ')
        sys.stdout.flush()

        print('| %6.2f ' % measure('numpy_eigvals(a)',repeat), end=' ')
        sys.stdout.flush()

        a = a[-1::-1,-1::-1]  # turn into a non-contiguous array
        assert_(not a.flags['CONTIGUOUS'])

        print('| %6.2f ' % measure('scipy_eigvals(a)',repeat), end=' ')
        sys.stdout.flush()

        print('| %6.2f ' % measure('numpy_eigvals(a)',repeat), end=' ')
        sys.stdout.flush()

        print('   (secs for %s calls)' % (repeat))
