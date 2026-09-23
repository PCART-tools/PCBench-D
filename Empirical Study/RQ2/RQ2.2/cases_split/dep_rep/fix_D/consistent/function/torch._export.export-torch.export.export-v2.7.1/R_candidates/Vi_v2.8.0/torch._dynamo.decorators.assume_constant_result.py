def assume_constant_result(fn):
    fn._dynamo_marked_constant = True
    return fn
