    def _detector_result(self) -> str:
        self.detector.close()
        result = self.detector.result["encoding"]
        if not result:  # pragma: nocover
            raise ValueError("Unable to determine encoding of content")

        return result
