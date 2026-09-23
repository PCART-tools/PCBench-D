    @final
    def _get_refs_and_copy(self, using_cow: bool, inplace: bool):
        refs = None
        copy = not inplace
        if inplace:
            if using_cow and self.refs.has_reference():
                copy = True
            else:
                refs = self.refs
        return copy, refs
