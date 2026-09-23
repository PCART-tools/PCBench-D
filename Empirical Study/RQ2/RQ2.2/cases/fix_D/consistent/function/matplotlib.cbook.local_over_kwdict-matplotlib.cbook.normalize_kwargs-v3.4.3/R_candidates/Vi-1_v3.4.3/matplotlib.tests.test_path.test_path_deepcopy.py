def test_path_deepcopy():
    # Should not raise any error
    verts = [[0, 0], [1, 1]]
    codes = [Path.MOVETO, Path.LINETO]
    path1 = Path(verts)
    path2 = Path(verts, codes)
    copy.deepcopy(path1)
    copy.deepcopy(path2)
