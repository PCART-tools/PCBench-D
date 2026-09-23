    def _process_values(self, input_data: dict) -> Dict[str, Any]:  # noqa: C901 (ignore complexity)
        return validate_model(self, input_data)
