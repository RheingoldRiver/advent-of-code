import pytest

from utils.grid import Grid, MoveError, Cell


def test_can_move():
    grid = Grid([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
    ])
    ptr = grid.new_pointer('ptr')
    ptr.move_to(0, 0)
    assert grid.width == 3
    assert grid.height == 4

    assert ptr.can_move_right() is True
    assert ptr.can_move_left() is False
    assert ptr.can_move_up() is False
    assert ptr.can_move_down() is True

    ptr.move_to(3, 2)
    assert ptr.can_move_right() is False
    assert ptr.can_move_left() is True
    assert ptr.can_move_up() is True
    assert ptr.can_move_down() is False

    ptr.move_to(1, 1)
    assert ptr.can_move_right() is True
    assert ptr.can_move_left() is True
    assert ptr.can_move_up() is True
    assert ptr.can_move_down() is True


def test_move():
    grid = Grid([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
    ])
    ptr = grid.new_pointer()
    ptr.move_to(1, 1)
    ptr.move_up()
    assert ptr.row == 0
    assert ptr.col == 1

    ptr.move_to(1, 1)
    ptr.move_down()
    assert ptr.row == 2
    assert ptr.col == 1

    ptr.move_to(1, 1)
    ptr.move_left()
    assert ptr.row == 1
    assert ptr.col == 0

    ptr.move_to(1, 1)
    ptr.move_right()
    assert ptr.row == 1
    assert ptr.col == 2

    ptr.move_to(1, 1)
    ptr.move_down(2)
    assert ptr.row == 3
    assert ptr.col == 1

    ptr.move_to(0, 0)
    with pytest.raises(MoveError) as e:
        ptr.move_up()
    assert str(e.value) == "Cannot move up!"

    ptr.move_to(0, 0)
    with pytest.raises(MoveError) as e:
        ptr.move_left()
    assert str(e.value) == "Cannot move left!"

    ptr.move_to(3, 2)
    with pytest.raises(MoveError) as e:
        ptr.move_down()
    assert str(e.value) == "Cannot move down!"

    ptr.move_to(3, 2)
    with pytest.raises(MoveError) as e:
        ptr.move_right()
    assert str(e.value) == "Cannot move right!"


def test_diagonal_move():
    grid = Grid([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
    ])
    ptr = grid.new_pointer('ptr')

    ptr.move_to(1, 1)
    ptr.move_down_right()
    assert ptr.row == 2
    assert ptr.col == 2

    ptr.move_to(1, 1)
    ptr.move_down_right(2, 1)
    assert ptr.cell == 12

    ptr.move_to(1, 1)
    with pytest.raises(MoveError) as e:
        ptr.move_down_right(3, 2)
    assert str(e.value) == "Cannot move down or right!"

    ptr.move_to(1, 1)
    ptr.move_down_left(1, 1)
    assert ptr.cell == 7

    ptr.move_to(1, 1)
    ptr.move_up_left(1, 1)
    assert ptr.cell == 1

    ptr.move_to(1, 1)
    ptr.move_up_right(1, 1)
    assert ptr.cell == 3

    ptr.move_to(1, 1)
    ptr.move_down_right(1, 1)
    assert ptr.cell == 9


def test_wrap_move():
    grid = Grid.read_from_array([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
    ])
    ptr = grid.new_pointer('ptr')
    ptr.move_to(1, 1)
    assert ptr.peek_up(1, True).data['value'] == 2
    assert ptr.peek_up(2, True).data['value'] == 17
    assert ptr.peek_up(3, True).data['value'] == 12
    assert ptr.peek_up(7, True).data['value'] == 12

    assert ptr.peek_left(1, True).data['value'] == 6
    assert ptr.peek_left(2, True).data['value'] == 10
    assert ptr.peek_left(7, True).data['value'] == 10

    assert ptr.peek_right(1, True).data['value'] == 8
    assert ptr.peek_right(2, True).data['value'] == 9
    assert ptr.peek_right(3, True).data['value'] == 10
    assert ptr.peek_right(4, True).data['value'] == 6
    assert ptr.peek_right(9, True).data['value'] == 6

    assert ptr.peek_down(2, True).data['value'] == 17
    assert ptr.peek_down(3, True).data['value'] == 2
    assert ptr.peek_down(7, True).data['value'] == 2


def test_neighbors():
    grid = Grid([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
    ])
    ptr = grid.new_pointer('ptr')
    ptr.move_to(1, 1)
    assert ptr.current_neighbors() == [12, 2, 6, 8]

    ptr.move_to(0, 0)
    assert ptr.current_neighbors() == [6, 2]

    ptr.move_to(1, 0)
    assert ptr.current_neighbors() == [11, 1, 7]

    ptr.move_to(0, 1)
    assert ptr.current_neighbors() == [7, 1, 3]

    ptr.move_to(0, 4)
    assert ptr.current_neighbors() == [10, 4]

    ptr.move_to(3, 4)
    assert ptr.current_neighbors() == [15, 19]


def test_peek_diagonal():
    grid = Grid([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
    ])
    ptr = grid.new_pointer('ptr')
    ptr.move_to(1, 1)
    assert ptr.peek_down_right(1, 1) == 13
    assert ptr.peek_up_left(1, 1) == 1
    assert ptr.peek_up_right(1, 1) == 3
    assert ptr.peek_down_left(1, 1) == 11
    assert ptr.peek_down_right(3, 1, True) == 3
    assert ptr.peek_down_left(3, 1, True) == 1
    assert ptr.peek_up_left(2, 1, True) == 16
    assert ptr.peek_up_right(2, 1, True) == 18


def test_generators():
    grid = Grid.read_from_array([
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
    ])
    assert list(grid.all_grid_cells())[7].data['value'] == 8
    assert list(grid.grid_cells_with_value(4))[0].data['value'] == 4
    assert list(grid.grid_cells_matching(lambda x: x.data['value'] % 2 == 0))[4].data['value'] == 10
    data = list(grid.grid_cells_matching(
        lambda x: (x.data['value'] % 2 == 0) and (x.row == 1)
    ))
    assert len(data) == 3
    assert data[1].data['value'] == 8
