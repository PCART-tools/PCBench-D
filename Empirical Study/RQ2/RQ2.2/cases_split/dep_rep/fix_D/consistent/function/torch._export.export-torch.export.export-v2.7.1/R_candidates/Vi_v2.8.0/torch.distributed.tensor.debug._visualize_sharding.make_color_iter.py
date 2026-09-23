def make_color_iter(color_map, num_rows, num_cols):
    num_colors = num_rows * num_cols
    for idx in range(num_colors):
        yield color_map(idx)
