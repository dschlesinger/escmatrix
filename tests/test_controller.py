from escmatrix.controller import TerminalBoard, Position, Unicode

def test_create_board() -> None:

    t = TerminalBoard()

    t[(slice(0, -1), slice(0, -1))] = Position(
        char=Unicode(char='A')
    )

