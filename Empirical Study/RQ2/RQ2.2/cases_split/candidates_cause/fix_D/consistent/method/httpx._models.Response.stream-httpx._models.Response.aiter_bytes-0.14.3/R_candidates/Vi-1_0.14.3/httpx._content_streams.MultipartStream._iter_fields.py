    def _iter_fields(
        self, data: typing.Mapping, files: RequestFiles
    ) -> typing.Iterator[typing.Union["FileField", "DataField"]]:
        for name, value in data.items():
            if isinstance(value, list):
                for item in value:
                    yield self.DataField(name=name, value=item)
            else:
                yield self.DataField(name=name, value=value)

        file_items = files.items() if isinstance(files, typing.Mapping) else files
        for name, value in file_items:
            yield self.FileField(name=name, value=value)
