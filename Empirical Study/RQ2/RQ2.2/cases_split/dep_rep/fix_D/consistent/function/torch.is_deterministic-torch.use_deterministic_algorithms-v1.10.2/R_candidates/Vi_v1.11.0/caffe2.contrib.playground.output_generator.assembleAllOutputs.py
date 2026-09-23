def assembleAllOutputs(self):
    output = {}
    output['train_model'] = self.train_model
    output['test_model'] = self.test_model
    output['model'] = self.model_output
    output['metrics'] = self.metrics_output
    return output
