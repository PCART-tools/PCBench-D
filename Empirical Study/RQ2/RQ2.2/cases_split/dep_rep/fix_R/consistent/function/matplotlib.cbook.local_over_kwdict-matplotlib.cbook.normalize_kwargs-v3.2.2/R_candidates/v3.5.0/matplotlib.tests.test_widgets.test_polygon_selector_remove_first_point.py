def test_polygon_selector_remove_first_point():
    verts = [(50, 50), (150, 50), (50, 150)]
    event_sequence = (polygon_place_vertex(*verts[0]) +
                      polygon_place_vertex(*verts[1]) +
                      polygon_place_vertex(*verts[2]) +
                      polygon_place_vertex(*verts[0]) +
                      polygon_remove_vertex(*verts[0]))
    check_polygon_selector(event_sequence, verts[1:], 2)
