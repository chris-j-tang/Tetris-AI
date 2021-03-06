import sys
import math


def _find_outline(board, down=False):
    """Find the outline of the top or bottom of the board."""
    counts = [0]*board.col_count()
    for c in board.cols():
        for cell in board.col_iter(c, reverse=down):
            if not cell:
                counts[c] += 1
            else:
                break
    return counts


def print_board(board, output=sys.stderr, entire=False, show_full=False):
    """Print a Tetris board."""
    try:
        rows = [r for r in board.rows(reverse=True, all=entire)]
    except TypeError:
        rows = [r for r in board.rows(reverse=True)]

    if rows and rows[0] > 1:
        row_format = '[%%s%%.%ud] ' % int(math.ceil(math.log(rows[0], 10)))
    else:
        row_format = '[%s%.1d] '

    for r in rows:
        modifier = None
        fill = None

        if show_full and all(cell for cell in board.row_iter(r)):
            fill = '~'

        try:
            if not modifier and board.is_fake_row(r):
                modifier = '@'
        except AttributeError:
            pass

        try:
            if not modifier and board.is_mirrored_row(r):
                modifier = '*'
        except AttributeError:
            pass

        if not modifier:
            modifier = ' '

        print >> output, row_format % (modifier, r), '|',
        for cell in board.row_iter(r):
            print >> output, fill if fill else (cell if cell else ' '),
        print >> output, '|'

    # (a bit of a hack, for spacing)
    print >> output, '-' * len(row_format % (0, 0)), '[',
    for c in board.cols():
        print >> output, c % 10,
    print >> output, ']'


def fill_board_with_zeros(bottom):
    """
    Takes a bottom portion of a tetris board with <20 rows
    and fills the rest of it up with 0's

    :param bottom: (Nx10 2-D List) The partial bottom of a Tetris board (where N < 20)
    :return: (20x10 2-D List) The partial bottom filled to 20 rows with 0's on top
    """
    rows_above = 20 - len(bottom)
    zero_row = [0]*10
    return [zero_row]*rows_above + bottom
