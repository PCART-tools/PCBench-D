@pytest.mark.skipif("not bokeh")
def test_unquote():
    from dask.diagnostics.profile_visualize import unquote
    from dask.delayed import to_task_dasks
    f = lambda x: to_task_dasks(x)[0]
    t = {'a': 1, 'b': 2, 'c': 3}
    assert unquote(f(t)) == t
    t = {'a': [1, 2, 3], 'b': 2, 'c': 3}
    assert unquote(f(t)) == t
    t = [1, 2, 3]
    assert unquote(f(t)) == t
