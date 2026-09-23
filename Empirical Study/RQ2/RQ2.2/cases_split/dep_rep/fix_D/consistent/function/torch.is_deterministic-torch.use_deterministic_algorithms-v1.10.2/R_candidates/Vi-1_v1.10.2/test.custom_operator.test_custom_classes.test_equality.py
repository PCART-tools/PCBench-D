def test_equality(f, cmp_key):
    obj1 = f()
    obj2 = jit.script(f)()
    return (cmp_key(obj1), cmp_key(obj2))
