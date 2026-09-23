def python_op_builder():
    PythonOpStats.lock.acquire()
    PythonOpStats.num_instances += 1
    PythonOpStats.lock.release()

    def my_op(inputs, outputs):
        PythonOpStats.lock.acquire()
        PythonOpStats.num_calls += 1
        PythonOpStats.lock.release()

    return my_op
