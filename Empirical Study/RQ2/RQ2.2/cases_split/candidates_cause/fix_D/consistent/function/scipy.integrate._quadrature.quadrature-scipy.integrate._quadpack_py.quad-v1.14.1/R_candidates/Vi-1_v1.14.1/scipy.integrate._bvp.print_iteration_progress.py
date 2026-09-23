def print_iteration_progress(iteration, residual, bc_residual, total_nodes,
                             nodes_added):
    print("{:^15}{:^15.2e}{:^15.2e}{:^15}{:^15}".format(
        iteration, residual, bc_residual, total_nodes, nodes_added))
