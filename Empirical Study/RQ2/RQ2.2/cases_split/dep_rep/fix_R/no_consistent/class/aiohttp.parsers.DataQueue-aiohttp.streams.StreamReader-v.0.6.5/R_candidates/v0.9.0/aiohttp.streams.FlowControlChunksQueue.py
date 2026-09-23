class FlowControlChunksQueue(FlowControlDataQueue, ChunksQueue):
    """FlowControlChunksQueue resumes and pauses an underlying stream."""

    readany = FlowControlDataQueue.read
