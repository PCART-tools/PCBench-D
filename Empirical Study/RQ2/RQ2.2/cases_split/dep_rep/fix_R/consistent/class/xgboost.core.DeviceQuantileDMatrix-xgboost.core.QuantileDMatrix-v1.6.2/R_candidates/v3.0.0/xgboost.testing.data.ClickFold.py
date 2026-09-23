@dataclass
class ClickFold:
    """A structure containing information about generated user-click data."""

    X: sparse.csr_matrix
    y: npt.NDArray[np.int32]
    qid: npt.NDArray[np.int32]
    score: npt.NDArray[np.float32]
    click: npt.NDArray[np.int32]
    pos: npt.NDArray[np.int64]
