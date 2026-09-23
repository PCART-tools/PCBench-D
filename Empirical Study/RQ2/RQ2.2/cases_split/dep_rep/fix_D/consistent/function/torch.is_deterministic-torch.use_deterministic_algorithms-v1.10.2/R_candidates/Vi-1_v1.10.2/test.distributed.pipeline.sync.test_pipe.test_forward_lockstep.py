def test_forward_lockstep(setup_rpc):
    timeline = []

    class DelayedLog(nn.Module):
        def __init__(self, j, seconds):
            super().__init__()
            self.i = 0
            self.j = j
            self.seconds = seconds

        def forward(self, x):
            time.sleep(self.seconds)

            timeline.append((self.i, self.j))
            self.i += 1

            return x

    model = nn.Sequential(DelayedLog(0, seconds=0), DelayedLog(1, seconds=0.1))
    model = Pipe(model, chunks=3)
    model(torch.rand(3, 1))

    # Expected timeline: (Logs are recorded at !)
    #
    # Partition #0: 0! 1!   2!
    # Partition #1:    000! 111! 222!
    #
    assert timeline == [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (2, 1)]
