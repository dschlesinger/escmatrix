from escmatrix.controller import TerminalBoard, Position, Unicode
from escmatrix import HexColor

from time import sleep

def test_create_board() -> None:

    print()

    t = TerminalBoard()

    t[(slice(0, -1), slice(0, -1))] = Position(
        char=Unicode(char='A')
    )

    t[(slice(0, -1), 0)] = Position(
        char=Unicode(char='B'),
        text_handler=HexColor.RED,
    )

    for i in range(min(t.R, t.C)):

        t[(i, i)] = Position(
            char=Unicode(char='C'),
            text_handler=HexColor.BLUE,
        )

    print(t.display())

