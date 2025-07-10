import signal, os, time

from escmatrix.terminal_tools import terminal_dims, reset_terminal
from escmatrix.color import ColorText, ColorBackground, TextHandler, BackgroundHandler

from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, Dict, Tuple, List

def get_end(s: slice, length: int) -> int:

    end = (s.stop if s.stop > 0 else length - s.stop - 1) if s.stop else length

    return end

def range_to_shape(s: slice, length: int) -> int:

    start = s.start or 0
    end = get_end(s, length)
    step = s.step or 1

    return (end - start) // step

class Unicode(BaseModel):

    char: str

    @field_validator('char', mode='after')
    def is_unicode(cls, char: str) -> str:

        if len(char) != 1:

            raise ValueError('{char} is not a unicode char, not len 1')
        
        return char

class Position(BaseModel):
    """For individual squares"""

    char: Unicode
    
    text_handler: TextHandler | None = None
    background_handler: BackgroundHandler | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class TerminalBoard(BaseModel):

    R: int = 0
    C: int = 0
    terminal_board: List[Position] = []

    def model_post_init(self, __context: Optional[Dict] = None) -> None:

        self.R, self.C = terminal_dims()

        self.terminal_board = [Position(char=Unicode(char=' '))] * (self.R * self.C)

        return
    
    def __getitem__(self, idx: Tuple[int | slice, int | slice]) -> Position | List[Position] | List[List[Position]]:
        """index with board[row, col]"""

        row, col = idx

        if isinstance(row, slice):

            row = range(row.start or 0, get_end(row, self.R), row.step or 1)
        
        else:
            # is int
            row = [row if row >= 0 else self.R - 1]

        if isinstance(col, slice):

            col = range(col.start or 0, get_end(col, self.C), col.step or 1)
        
        else:
            # is int
            col = [col if col >= 0 else self.C - 1]

        board_part: List[List[Position]] = []

        for r in row:

            row_part: List[Position] = []

            for c in col:

                row_part.append(self.terminal_board[r * self.C + c])

            board_part.append(row_part)
        
        for _ in range(2):

            if len(board_part) == 1:

                board_part = board_part[0]
            
            else:

                break

        return board_part
    
    def __setitem__(self, idx: Tuple[int | slice, int | slice], item: Position | List[Position] | List[List[Position]]) -> None:
        """Set item into board

        Args:
            idx (Tuple[int | slice, int | slice]): can be slice or int
            item (Position | List[Position] | List[List[Position]]): Can cast if singlular
        """        

        assign_shape: Tuple[int, int] = (
            1 if isinstance(idx[0], int) else range_to_shape(idx[0], self.R),
            1 if isinstance(idx[1], int) else range_to_shape(idx[1], self.C),
        )

        # Assumes uniform
        data_shape: Tuple[int, int] = (0, 0)

        cast: bool = False

        if isinstance(item, Position):

            data_shape = (1, 1)

            cast = True
        
        elif isinstance(item[0], Position):

            data_shape = (len(item), 1)

        else:

            data_shape = (len(item), len(item[0]))
        
        assert data_shape == assign_shape or data_shape == (1, 1), f"Assign shape {assign_shape} does not match data shape {data_shape}"

        # Nest data to 2 dim list
        if not cast:
            for s in data_shape:

                if s == 1:

                    item = [item]

        row, col = idx

        if isinstance(row, slice):

            row = range(row.start or 0, get_end(row, self.R), row.step or 1)
        
        else:
            # is int
            row = [row if row >= 0 else self.R - 1]

        if isinstance(col, slice):

            col = range(col.start or 0, get_end(col, self.C), col.step or 1)
        
        else:
            # is int
            col = [col if col >= 0 else self.C - 1]
        
        for r in row:

            for c in col:

                self.terminal_board[r * self.C + c] = item if cast else item[r][c]

        return
    
    def display(self) -> str:

        board: str = ''

        for r in range(self.R):
            for c in range(self.C):

                p = self.terminal_board[r * self.C + c]

                t = p.char.char

                if (th := p.text_handler) is not None:

                    t = th.apply(t)

                if (bh := p.background_handler) is not None:

                    t = bh.apply(t)

                board += t

            if r < self.R - 1:
            
                board += '\n'

        return board
        
    def refresh(self) -> None:

        print(self.display(), end='')

        reset_terminal()

if __name__ == '__main__':

    board = TerminalBoard()

    board[(slice(0, -1), slice(0, -1))] = Position(
        char=Unicode(char='A')
    )

    board[(0, slice(0, -1))] = Position(
        char=Unicode(char='C'),
        text_handler=ColorText.EscapeColor.RED,
    )

    board[(slice(0, -1), 0)] = Position(
        char=Unicode(char='C'),
        text_handler=ColorText.EscapeColor.BLUE,
    )

    board.refresh()