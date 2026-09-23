def example_task():
    with Task():
        with ops.task_init():
            one = ops.Const(1)
        two = ops.Add([one, one])
        with ops.task_init():
            three = ops.Const(3)
        accum = ops.Add([two, three])
        # here, accum should be 5
        with ops.task_exit():
            # here, accum should be 6, since this executes after lines below
            seven_1 = ops.Add([accum, one])
        six = ops.Add([accum, one])
        ops.Add([accum, one], [accum])
        seven_2 = ops.Add([accum, one])
        o6 = final_output(six)
        o7_1 = final_output(seven_1)
        o7_2 = final_output(seven_2)

    with Task(num_instances=2):
        with ops.task_init():
            one = ops.Const(1)
        with ops.task_instance_init():
            local = ops.Const(2)
        ops.Add([one, local], [one])
        ops.LogInfo('ble')

    return o6, o7_1, o7_2
