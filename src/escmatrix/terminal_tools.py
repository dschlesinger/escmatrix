import shutil
from typing import Tuple

from time import sleep

def terminal_dims() -> Tuple[int, int]:
    """Returns (#Rows, #Columns)"""

    C, R = shutil.get_terminal_size()

    return (R, C)

def reset_terminal() -> None:
    print('\033[H', end='')

if __name__ == '__main__':

    reset_terminal()

    sleep(2)

    print('(This is where it will be)')
