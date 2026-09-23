def print_iteration_linear(iteration, cost, cost_reduction, step_norm,
                           optimality):
    if cost_reduction is None:
        cost_reduction = " " * 15
    else:
        cost_reduction = "{0:^15.2e}".format(cost_reduction)

    if step_norm is None:
        step_norm = " " * 15
    else:
        step_norm = "{0:^15.2e}".format(step_norm)

    print("{0:^15}{1:^15.4e}{2}{3}{4:^15.2e}".format(
        iteration, cost, cost_reduction, step_norm, optimality))
