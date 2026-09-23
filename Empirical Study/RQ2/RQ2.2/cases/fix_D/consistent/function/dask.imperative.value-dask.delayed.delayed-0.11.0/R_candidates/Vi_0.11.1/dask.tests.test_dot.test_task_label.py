def test_task_label():
    assert task_label((partial(add, 1), 1)) == 'add'
    assert task_label((add, 1)) == 'add'
    assert task_label((add, (add, 1, 2))) == 'add(...)'
