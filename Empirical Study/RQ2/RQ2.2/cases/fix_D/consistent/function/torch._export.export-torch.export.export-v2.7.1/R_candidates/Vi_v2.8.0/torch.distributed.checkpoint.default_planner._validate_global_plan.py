def _validate_global_plan(global_plan: list[SavePlan], metadata: Metadata) -> bool:
    all_good = True
    for key, value in metadata.state_dict_metadata.items():
        if isinstance(value, BytesStorageMetadata):
            continue
        if len(value.size) == 0:
            continue
        chunks_volume = 0
        for chunk_idx, chunk0 in enumerate(value.chunks):
            # Compute the volume
            if not _check_box_bounds(value.size, chunk0):
                logger.warning(
                    """
                        key:%s has out of bounds chunk:
                        tensor-size:%s chunk: %s
                    """,
                    key,
                    value.size,
                    chunk0,
                )
                all_good = False
            chunks_volume += reduce(operator.mul, chunk0.sizes, 1)

            # Check for overlap
            for chunk1 in value.chunks[chunk_idx + 1 :]:
                if _check_box_overlap(chunk0, chunk1):
                    logger.warning(
                        "key:%s has overlapping chunks: %s %s", key, chunk0, chunk1
                    )
                    all_good = False

        # Check whether combined chunk cover the whole tensor
        tensor_volume = reduce(operator.mul, value.size, 1)
        if chunks_volume != tensor_volume:
            logger.warning(
                """
                    key:%s invalid fill tensor-volume:
                    %s chunks-volume: %s
                """,
                key,
                tensor_volume,
                chunks_volume,
            )
            all_good = False

    return all_good
