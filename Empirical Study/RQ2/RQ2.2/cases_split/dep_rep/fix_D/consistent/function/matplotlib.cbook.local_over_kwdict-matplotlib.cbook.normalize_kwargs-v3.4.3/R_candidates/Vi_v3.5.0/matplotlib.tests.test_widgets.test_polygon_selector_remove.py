@pytest.mark.parametrize('idx', [1, 2, 3])
def test_polygon_selector_remove(idx):
    verts = [(50, 50), (150, 50), (50, 150)]
    event_sequence = [polygon_place_vertex(*verts[0]),
                      polygon_place_vertex(*verts[1]),
                      polygon_place_vertex(*verts[2]),
                      # Finish the polygon
                      polygon_place_vertex(*verts[0])]
    # Add an extra point
    event_sequence.insert(idx, polygon_place_vertex(200, 200))
    # Remove the extra point
    event_sequence.append(polygon_remove_vertex(200, 200))
    # Flatten list of lists
    event_sequence = sum(event_sequence, [])
    check_polygon_selector(event_sequence, verts, 2)
