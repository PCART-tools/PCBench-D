def register_fake_classes():
    # noqa: F841
    @torch._library.register_fake_class("_TorchScriptTesting::_Foo")
    class FakeFoo:
        def __init__(self, x: int, y: int):
            self.x = x
            self.y = y

        @classmethod
        def __obj_unflatten__(cls, flattend_foo):
            return cls(**dict(flattend_foo))

        def add_tensor(self, z):
            return (self.x + self.y) * z

    @torch._library.register_fake_class("_TorchScriptTesting::_ContainsTensor")
    class FakeContainsTensor:
        def __init__(self, t: torch.Tensor):
            self.t = t

        @classmethod
        def __obj_unflatten__(cls, flattend_foo):
            return cls(**dict(flattend_foo))

        def get(self):
            return self.t
