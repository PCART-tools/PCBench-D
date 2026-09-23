def test_ndependents():
    a, b, c = 'abc'
    dsk = dict(chain((((a, i), i * 2) for i in range(5)),
                     (((b, i), (add, i, (a, i))) for i in range(5)),
                     (((c, i), (add, i, (b, i))) for i in range(5))))
    result = ndependents(*get_deps(dsk))
    expected = dict(chain((((a, i), 3) for i in range(5)),
                          (((b, i), 2) for i in range(5)),
                          (((c, i), 1) for i in range(5))))
    assert result == expected

    dsk = {a: 1, b: 1}
    deps = get_deps(dsk)
    assert ndependents(*deps) == dsk

    dsk = {a: 1, b: (add, a, 1), c: (add, b, a)}
    assert ndependents(*get_deps(dsk)) == {a: 4, b: 2, c: 1}

    dsk = {a: 1, b: a, c: b}
    deps = get_deps(dsk)
    assert ndependents(*deps) == {a: 3, b: 2, c: 1}
