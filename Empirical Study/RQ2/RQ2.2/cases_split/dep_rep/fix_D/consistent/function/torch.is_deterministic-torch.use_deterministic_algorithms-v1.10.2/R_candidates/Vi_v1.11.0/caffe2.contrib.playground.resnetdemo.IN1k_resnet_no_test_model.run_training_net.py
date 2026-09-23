def run_training_net(self):
    timeout = 2000.0
    with timeout_guard.CompleteInTimeOrDie(timeout):
        workspace.RunNet(self.train_model.net.Proto().name)
