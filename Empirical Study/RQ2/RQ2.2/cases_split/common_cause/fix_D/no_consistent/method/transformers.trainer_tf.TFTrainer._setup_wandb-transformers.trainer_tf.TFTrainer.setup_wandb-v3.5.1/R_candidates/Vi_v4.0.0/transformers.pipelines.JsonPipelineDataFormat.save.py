    def save(self, data: dict):
        """
        Save the provided data object in a json file.

        Args:
            data (:obj:`dict`): The data to store.
        """
        with open(self.output_path, "w") as f:
            json.dump(data, f)
