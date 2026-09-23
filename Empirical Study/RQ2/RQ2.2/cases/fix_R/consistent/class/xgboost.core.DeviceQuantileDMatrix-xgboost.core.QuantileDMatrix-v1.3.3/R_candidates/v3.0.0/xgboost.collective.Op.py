@unique
class Op(IntEnum):
    """Supported operations for allreduce."""

    MAX = 0
    MIN = 1
    SUM = 2
    BITWISE_AND = 3
    BITWISE_OR = 4
    BITWISE_XOR = 5
