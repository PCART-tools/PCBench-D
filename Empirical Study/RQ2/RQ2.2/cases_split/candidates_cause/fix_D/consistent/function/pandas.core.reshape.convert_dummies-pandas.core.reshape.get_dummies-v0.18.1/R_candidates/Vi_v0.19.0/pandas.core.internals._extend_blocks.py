def _extend_blocks(result, blocks=None):
    """ return a new extended blocks, givin the result """
    if blocks is None:
        blocks = []
    if isinstance(result, list):
        for r in result:
            if isinstance(r, list):
                blocks.extend(r)
            else:
                blocks.append(r)
    elif isinstance(result, BlockManager):
        blocks.extend(result.blocks)
    else:
        blocks.append(result)
    return blocks
