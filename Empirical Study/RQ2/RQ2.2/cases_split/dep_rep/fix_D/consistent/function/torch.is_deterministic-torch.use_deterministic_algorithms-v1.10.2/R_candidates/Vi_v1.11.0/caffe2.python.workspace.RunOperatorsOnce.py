def RunOperatorsOnce(operators):
    for op in operators:
        success = RunOperatorOnce(op)
        if not success:
            return False
    return True
