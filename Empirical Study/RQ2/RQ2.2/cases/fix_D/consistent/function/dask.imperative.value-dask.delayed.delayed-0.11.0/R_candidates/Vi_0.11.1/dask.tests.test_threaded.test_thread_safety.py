def test_thread_safety():
    def f(x):
        return 1

    dsk = {'x': (sleep, 0.05), 'y': (f, 'x')}

    L = []

    def test_f():
        L.append(get(dsk, 'y'))

    threads = []
    for i in range(20):
        t = Thread(target=test_f)
        t.daemon = True
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    assert L == [1] * 20
