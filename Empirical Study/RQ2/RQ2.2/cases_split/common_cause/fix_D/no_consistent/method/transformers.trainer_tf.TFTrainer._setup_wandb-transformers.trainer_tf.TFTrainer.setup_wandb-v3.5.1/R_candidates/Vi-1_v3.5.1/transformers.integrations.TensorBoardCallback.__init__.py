    def __init__(self, tb_writer=None):
        assert (
            _has_tensorboard
        ), "TensorBoardCallback requires tensorboard to be installed. Either update your PyTorch version or install tensorboardX."
        self.tb_writer = tb_writer
