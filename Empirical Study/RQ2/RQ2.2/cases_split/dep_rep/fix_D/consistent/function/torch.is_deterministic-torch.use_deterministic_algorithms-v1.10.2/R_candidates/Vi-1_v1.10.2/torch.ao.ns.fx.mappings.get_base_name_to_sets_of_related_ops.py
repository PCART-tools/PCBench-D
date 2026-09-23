def get_base_name_to_sets_of_related_ops() -> Dict[str, Set[NSNodeTargetType]]:
    sets_of_related_ops: List[Set[NSNodeTargetType]] = [
        # conv modules
        set([
            nn.Conv1d,
            nnq.Conv1d,
            nniqat.ConvBn1d,
            nniqat.ConvBnReLU1d,
            nniq.ConvReLU1d,
            nni.ConvReLU1d,
        ]),
        set([
            nn.Conv2d,
            nnq.Conv2d,
            nnqat.Conv2d,
            nniqat.ConvBn2d,
            nniqat.ConvBnReLU2d,
            nniqat.ConvReLU2d,
            nniq.ConvReLU2d,
            nni.ConvReLU2d,
        ]),
        set([
            nn.Conv3d,
            nnq.Conv3d,
            nnqat.Conv3d,
            nniqat.ConvBn3d,
            nniqat.ConvBnReLU3d,
            nniqat.ConvReLU3d,
            nniq.ConvReLU3d,
            nni.ConvReLU3d,
        ]),
        # conv functionals
        set([
            F.conv1d,
            toq.conv1d,
            toq.conv1d_relu,
        ]),
        set([
            F.conv2d,
            toq.conv2d,
            toq.conv2d_relu,
        ]),
        set([
            F.conv3d,
            toq.conv3d,
            toq.conv3d_relu,
        ]),
        # linear modules
        set([
            nn.Linear,
            nnq.Linear,
            nni.LinearReLU,
            nniq.LinearReLU,
            nniqd.LinearReLU,
            nnqat.Linear,
            nnqd.Linear,
            nniqat.LinearReLU,
            nn.modules.linear.NonDynamicallyQuantizableLinear,
        ]),
        # linear functionals
        set([
            F.linear,
            toq.linear,
            toq.linear_relu,
        ]),
        # average pool
        set([
            nn.AvgPool1d,
            torch.avg_pool1d,
        ]),
        set([
            nn.AvgPool2d,
            torch._C._nn.avg_pool2d,
        ]),
        set([
            nn.AvgPool3d,
            torch._C._nn.avg_pool3d,
        ]),
        # adaptive average pool
        set([
            nn.AdaptiveAvgPool1d,
            F.adaptive_avg_pool1d,
        ]),
        set([
            nn.AdaptiveAvgPool2d,
            F.adaptive_avg_pool2d,
        ]),
        set([
            nn.AdaptiveAvgPool3d,
            F.adaptive_avg_pool3d,
        ]),
        # LSTM
        set([
            nn.LSTM,
            nnqd.LSTM,
        ]),
        # add
        set([
            torch.add,
            toq.add,
            operator.add,  # x + y
            toq.add_relu,
        ]),
        # cat
        set([
            torch.cat,
            toq.cat,
        ]),
        # mul
        set([
            torch.mul,
            toq.mul,
            operator.mul,
            toq.mul_relu,
        ]),
        # relu
        set([
            F.relu,
            nn.ReLU,
            'relu',
            'relu_',
            torch.relu,
        ]),
        # maxpool
        set([
            nn.MaxPool1d,
            F.max_pool1d,
        ]),
        set([
            nn.MaxPool2d,
            F.max_pool2d,
        ]),
        set([
            nn.MaxPool3d,
            F.max_pool3d,
        ]),
        # sigmoid
        set([
            torch.sigmoid,
            'sigmoid',
            'sigmoid_',
            nn.Sigmoid,
            F.sigmoid,
        ]),
        # BatchNorm
        set([
            nn.BatchNorm2d,
            nnq.BatchNorm2d,
        ]),
        set([
            nn.BatchNorm3d,
            nnq.BatchNorm3d,
        ]),
        # ConvTranspose
        set([
            nn.ConvTranspose1d,
            nnq.ConvTranspose1d,
        ]),
        set([
            nn.ConvTranspose2d,
            nnq.ConvTranspose2d,
        ]),
        # ELU
        set([
            nn.ELU,
            nnq.ELU,
        ]),
        # Embedding
        set([
            nn.Embedding,
            nnq.Embedding,
        ]),
        # EmbeddingBag
        set([
            nn.EmbeddingBag,
            nnq.EmbeddingBag,
        ]),
        # GroupNorm
        set([
            nn.GroupNorm,
            nnq.GroupNorm,
        ]),
        # Hardswish
        set([
            nn.Hardswish,
            nnq.Hardswish,
        ]),
        # InstanceNorm
        set([
            nn.InstanceNorm1d,
            nnq.InstanceNorm1d,
        ]),
        set([
            nn.InstanceNorm2d,
            nnq.InstanceNorm2d,
        ]),
        set([
            nn.InstanceNorm3d,
            nnq.InstanceNorm3d,
        ]),
        # LayerNorm
        set([
            nn.LayerNorm,
            nnq.LayerNorm,
        ]),
        # LeakyReLU
        set([
            nn.LeakyReLU,
            nnq.LeakyReLU,
        ]),
        # ReLU6
        set([
            nn.ReLU6,
            F.relu6,
            nnq.ReLU6,
        ]),
        # BNReLU2d
        set([
            nni.BNReLU2d,
            nniq.BNReLU2d,
        ]),
        set([
            nni.BNReLU3d,
            nniq.BNReLU3d,
        ]),
        # F.elu
        set([
            F.elu,
            toq.elu,
        ]),
        # F.hardswish
        set([
            F.hardswish,
            toq.hardswish,
        ]),
        # F.instance_norm
        set([
            F.instance_norm,
            toq.instance_norm,
        ]),
        # F.layer_norm
        set([
            F.layer_norm,
            toq.layer_norm,
        ]),
        # F.leaky_relu
        set([
            F.leaky_relu,
            toq.leaky_relu,
        ]),
        # F.silu
        set([
            nn.SiLU,
            F.silu,
        ]),
        # F.mish
        set([
            nn.Mish,
            F.mish,
        ]),
        # F.tanh
        set([
            nn.Tanh,
            F.tanh,
            torch.tanh,
            'tanh_',
            'tanh',
        ]),
        # F.hardsigmoid
        set([
            'hardsigmoid_',
            'hardsigmoid',
            F.hardsigmoid,
            nn.Hardsigmoid,
        ]),
        # F.hardtanh
        set([
            nn.Hardtanh,
            F.hardtanh,
            F.hardtanh_,
        ]),
        # floordiv
        set([
            operator.floordiv,
        ]),
        # unsqueeze
        set([
            torch.unsqueeze,
        ]),
        # stack
        set([
            torch.stack,
        ]),
        # squeeze
        set([
            torch.squeeze,
        ]),
        # sort
        set([
            torch.sort,
        ]),
        # repeat_interleave
        set([
            torch.repeat_interleave,
        ]),
        # min
        set([
            torch.min,
        ]),
        # mean
        set([
            torch.mean,
        ]),
        # max
        set([
            torch.max,
        ]),
        # transpose
        set([
            torch.transpose,
        ]),
        # flatten
        set([
            torch.flatten,
        ]),
        # clamp
        set([
            torch.clamp,
        ]),
        # chunk
        set([
            torch.chunk,
        ]),
        # interpolate
        set([
            torch.nn.functional.interpolate,
        ]),
        # dropout
        set([
            nn.Dropout,
            F.dropout,
        ]),
    ]

    base_name_to_sets_of_related_ops: Dict[str, Set[NSNodeTargetType]] = {}

    counter = 0
    for set_of_related_ops in sets_of_related_ops:
        base_name = str(counter)
        counter += 1
        base_name_to_sets_of_related_ops[base_name] = set_of_related_ops

    return base_name_to_sets_of_related_ops
