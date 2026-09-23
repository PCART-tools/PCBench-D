def test_threaded_within_thread():
    L = []
    def f(i):
        result = get({'x': (lambda: i,)}, 'x', num_workers=2)
        L.append(result)

    before = threading.active_count()

    for i in range(20):
        t = Thread(target=f, args=(1,))
        t.daemon = True
        t.start()
        t.join()
        assert L == [1]
        del L[:]

    start = time()  # wait for most threads to join
    while threading.active_count() > before + 10:
        sleep(0.01)
        assert time() < start + 5
