    def create_tensor_descriptor_shim(
        tensor, block_sizes: list[int], new_api: bool = True
    ):
        if new_api:
            return triton.tools.tensor_descriptor.TensorDescriptor.from_tensor(
                tensor, block_sizes
            )
        else:
            if len(block_sizes) == 1:
                return triton.tools.experimental_descriptor.create_1d_tma_descriptor(
                    tensor.data_ptr(),
                    tensor.size(0),
                    block_sizes[0],
                    tensor.element_size(),
                )
            else:
                assert len(block_sizes) == 2
                return triton.tools.experimental_descriptor.create_2d_tma_descriptor(
                    tensor.data_ptr(),
                    tensor.size(0),
                    tensor.size(1),
                    block_sizes[0],
                    block_sizes[1],
                    tensor.element_size(),
                )
