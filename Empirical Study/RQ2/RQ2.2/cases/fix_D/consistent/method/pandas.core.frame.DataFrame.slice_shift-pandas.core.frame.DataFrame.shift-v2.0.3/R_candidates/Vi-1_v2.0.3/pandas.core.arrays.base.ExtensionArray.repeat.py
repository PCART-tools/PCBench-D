    @Substitution(klass="ExtensionArray")
    @Appender(_extension_array_shared_docs["repeat"])
    def repeat(
        self: ExtensionArrayT, repeats: int | Sequence[int], axis: AxisInt | None = None
    ) -> ExtensionArrayT:
        nv.validate_repeat((), {"axis": axis})
        ind = np.arange(len(self)).repeat(repeats)
        return self.take(ind)
