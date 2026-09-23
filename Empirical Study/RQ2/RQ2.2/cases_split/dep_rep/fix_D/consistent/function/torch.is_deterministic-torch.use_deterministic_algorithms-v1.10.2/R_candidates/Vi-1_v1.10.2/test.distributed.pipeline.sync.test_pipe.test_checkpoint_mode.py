def test_checkpoint_mode(setup_rpc):
    def count_grad_fn(grad_fn, name, visited=None):
        if visited is None:
            visited = set()
        if grad_fn in visited:
            return 0
        visited.add(grad_fn)

        if grad_fn is None:
            return 0
        if grad_fn.__class__.__name__ == name:
            return 1

        counter = 0
        for next_grad_fn, _ in grad_fn.next_functions:
            counter += count_grad_fn(next_grad_fn, name, visited=visited)
        return counter

    model = nn.Sequential(nn.Linear(1, 1))
    input = torch.rand(2, 1)

    always = Pipe(model, chunks=2, checkpoint="always")
    except_last = Pipe(model, chunks=2, checkpoint="except_last")
    never = Pipe(model, chunks=2, checkpoint="never")

    always_output = always(input)
    except_last_output = except_last(input)
    never_output = never(input)

    assert count_grad_fn(always_output.local_value().grad_fn, "CheckpointBackward") == 2
    assert count_grad_fn(except_last_output.local_value().grad_fn, "CheckpointBackward") == 1
    assert count_grad_fn(never_output.local_value().grad_fn, "CheckpointBackward") == 0
