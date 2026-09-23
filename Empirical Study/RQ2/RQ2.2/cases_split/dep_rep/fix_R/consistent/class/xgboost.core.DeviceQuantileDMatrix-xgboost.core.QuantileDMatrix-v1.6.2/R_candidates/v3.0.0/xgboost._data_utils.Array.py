    class Array:
        """Wrapper type for communicating with numpy and cupy."""

        _interface: Optional[ArrayInf] = None

        @property
        def __array_interface__(self) -> Optional[ArrayInf]:
            return self._interface

        @__array_interface__.setter
        def __array_interface__(self, interface: ArrayInf) -> None:
            self._interface = copy.copy(interface)
            # Convert some fields to tuple as required by numpy
            self._interface["shape"] = tuple(self._interface["shape"])
            self._interface["data"] = (
                self._interface["data"][0],
                self._interface["data"][1],
            )
            strides = self._interface.get("strides", None)
            if strides is not None:
                self._interface["strides"] = tuple(strides)

        @property
        def __cuda_array_interface__(self) -> Optional[ArrayInf]:
            return self.__array_interface__

        @__cuda_array_interface__.setter
        def __cuda_array_interface__(self, interface: ArrayInf) -> None:
            self.__array_interface__ = interface
