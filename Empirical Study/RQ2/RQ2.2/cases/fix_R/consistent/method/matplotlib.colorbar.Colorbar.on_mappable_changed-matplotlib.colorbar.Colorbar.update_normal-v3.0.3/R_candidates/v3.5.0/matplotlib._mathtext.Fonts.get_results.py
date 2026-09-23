    def get_results(self, box):
        """
        Get the data needed by the backend to render the math
        expression.  The return value is backend-specific.
        """
        result = self.mathtext_backend.get_results(
            box, self.get_used_characters())
        if self.destroy != TruetypeFonts.destroy.__get__(self):
            destroy = _api.deprecate_method_override(
                __class__.destroy, self, since="3.4")
            if destroy:
                destroy()
        return result
