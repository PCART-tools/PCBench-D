    def get_results(self, box):
        """
        Get the data needed by the backend to render the math
        expression.  The return value is backend-specific.
        """
        result = self.mathtext_backend.get_results(box, self.get_used_characters())
        self.destroy()
        return result
