def _make_lightning_module(iC: int, oC: list[int]):
    import pytorch_lightning as pl  # type: ignore[import]

    class DummyLightningModule(pl.LightningModule):
        def __init__(self, ic: int, oC: list[int]):
            super().__init__()
            self.model = DummyModel(iC, oC)

        def forward(self):
            pass

    return DummyLightningModule(iC, oC)
