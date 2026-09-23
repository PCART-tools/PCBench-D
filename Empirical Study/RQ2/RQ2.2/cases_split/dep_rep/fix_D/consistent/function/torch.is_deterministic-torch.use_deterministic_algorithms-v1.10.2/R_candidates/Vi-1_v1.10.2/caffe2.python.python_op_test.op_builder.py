def op_builder(name, index, extra):
    iterations = [0]
    assert name == 'name'
    assert index == 5
    assert extra - 4.2 < 0.0001

    def my_op(inputs, outputs):
        assert inputs[0].data[0] == iterations[0]
        assert name == 'name'
        assert index == 5
        assert extra - 4.2 < 0.0001
        iterations[0] += 1

    return my_op
