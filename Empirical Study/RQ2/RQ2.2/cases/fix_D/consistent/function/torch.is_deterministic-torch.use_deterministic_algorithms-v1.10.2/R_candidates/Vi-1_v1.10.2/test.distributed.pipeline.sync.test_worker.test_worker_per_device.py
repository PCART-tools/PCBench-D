def test_worker_per_device():
    cpu = torch.device("cpu")
    cpu0 = torch.device("cpu", index=0)
    fake1 = fake_device()
    fake2 = fake_device()

    with spawn_workers([cpu, cpu, cpu0, fake1, fake2]) as (in_queues, out_queues):
        assert len(in_queues) == len(out_queues) == 5

        # 0: cpu, 1: cpu, 2: cpu0
        assert in_queues[0] is in_queues[1] is in_queues[2]
        assert out_queues[0] is out_queues[1] is out_queues[2]

        # 3: fake1, 4: fake2
        assert in_queues[3] is not in_queues[4]
        assert out_queues[3] is not out_queues[4]
