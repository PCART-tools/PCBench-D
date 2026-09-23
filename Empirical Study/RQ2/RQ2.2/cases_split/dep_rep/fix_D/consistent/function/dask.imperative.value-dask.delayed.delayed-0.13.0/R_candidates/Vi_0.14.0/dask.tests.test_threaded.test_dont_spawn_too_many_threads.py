def test_dont_spawn_too_many_threads():
    before = threading.active_count()

    dsk = {('x', i): (lambda: i,) for i in range(10)}
    dsk['x'] = (sum, list(dsk))
    for i in range(20):
        get(dsk, 'x', num_workers=4)

    after = threading.active_count()

    assert after <= before + 8
