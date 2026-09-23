    def __init__(self, azureml_run=None):
        assert _has_azureml, "AzureMLCallback requires azureml to be installed. Run `pip install azureml-sdk`."
        self.azureml_run = azureml_run
