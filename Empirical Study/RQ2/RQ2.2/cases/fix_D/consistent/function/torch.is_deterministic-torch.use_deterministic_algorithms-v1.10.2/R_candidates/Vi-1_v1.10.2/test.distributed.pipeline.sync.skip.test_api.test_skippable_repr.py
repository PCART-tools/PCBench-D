def test_skippable_repr():
    @skippable(stash=["hello"])
    class Hello(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Conv2d(1, 1, 1)

        def forward(self, x):
            yield stash("hello", x)
            return self.conv(x)  # noqa: B901

    m = Hello()
    assert (
        repr(m)
        == """
@skippable(Hello(
  (conv): Conv2d(1, 1, kernel_size=(1, 1), stride=(1, 1))
))
""".strip()
    )
