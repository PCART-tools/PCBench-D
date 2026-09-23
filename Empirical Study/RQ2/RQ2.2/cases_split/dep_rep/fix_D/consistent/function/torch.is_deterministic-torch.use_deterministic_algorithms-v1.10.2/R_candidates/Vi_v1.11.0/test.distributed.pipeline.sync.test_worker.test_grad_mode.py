@pytest.mark.parametrize("grad_mode", [True, False])
def test_grad_mode(grad_mode):
    def detect_grad_enabled():
        x = torch.rand(1, requires_grad=torch.is_grad_enabled())
        return Batch(x)

    with torch.set_grad_enabled(grad_mode):
        with spawn_workers([torch.device("cpu")]) as (in_queues, out_queues):
            task = Task(CPUStream, compute=detect_grad_enabled, finalize=None)
            in_queues[0].put(task)

            ok, (_, batch) = out_queues[0].get()

            assert ok
            assert batch[0].requires_grad == grad_mode
