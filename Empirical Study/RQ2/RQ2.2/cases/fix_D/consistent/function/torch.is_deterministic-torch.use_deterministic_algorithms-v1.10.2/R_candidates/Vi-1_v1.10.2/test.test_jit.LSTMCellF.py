def LSTMCellF(input, hx, cx, *params):
    return LSTMCell(input, (hx, cx), *params)
