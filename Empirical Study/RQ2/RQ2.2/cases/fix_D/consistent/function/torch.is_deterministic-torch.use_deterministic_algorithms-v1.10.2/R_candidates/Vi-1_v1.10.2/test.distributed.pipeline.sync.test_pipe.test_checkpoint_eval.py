def test_checkpoint_eval(setup_rpc):
    model = nn.Sequential(nn.Linear(1, 1))
    model = Pipe(model, chunks=2)
    input = torch.rand(2, 1)

    def find_grad_fn(grad_fn, name):
        if grad_fn is None:
            return False
        if grad_fn.__class__.__name__ == name:
            return True
        for next_grad_fn, _ in grad_fn.next_functions:
            if find_grad_fn(next_grad_fn, name):
                return True
        return False

    model.train()
    train_output = model(input)
    assert find_grad_fn(train_output.local_value().grad_fn, "CheckpointBackward")
    assert find_grad_fn(train_output.local_value().grad_fn, "RecomputeBackward")

    model.eval()
    eval_output = model(input)
    assert not find_grad_fn(eval_output.local_value().grad_fn, "CheckpointBackward")
    assert not find_grad_fn(eval_output.local_value().grad_fn, "RecomputeBackward")
