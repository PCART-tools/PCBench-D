def RunOperatorMultiple(operator, num_runs):
    return C.run_operator_multiple(StringifyProto(operator), num_runs)
