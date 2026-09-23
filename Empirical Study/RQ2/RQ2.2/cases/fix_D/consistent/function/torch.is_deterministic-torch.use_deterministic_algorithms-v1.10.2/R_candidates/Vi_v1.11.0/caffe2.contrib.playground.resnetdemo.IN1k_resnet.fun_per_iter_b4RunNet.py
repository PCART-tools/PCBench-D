def fun_per_iter_b4RunNet(self, epoch, epoch_iter):

    learning_rate = 0.05
    for idx in range(self.opts['distributed']['first_xpu_id'],
                     self.opts['distributed']['first_xpu_id'] +
                     self.opts['distributed']['num_xpus']):
        caffe2_pb2_device = caffe2_pb2.CUDA if \
            self.opts['distributed']['device'] == 'gpu' else \
            caffe2_pb2.CPU
        with core.DeviceScope(core.DeviceOption(caffe2_pb2_device, idx)):
            workspace.FeedBlob(
                '{}_{}/lr'.format(self.opts['distributed']['device'], idx),
                np.array(learning_rate, dtype=np.float32)
            )
