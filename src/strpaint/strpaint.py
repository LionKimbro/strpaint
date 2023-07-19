"""strpaint  -- 2-D string painting"""

import copy


X="X"
Y="Y"

CLIPX="CLIPX"
CLIPY="CLIPY"
CLIPX1="CLIPX1"
CLIPY1="CLIPY1"

TEMPLATE="TEMPLATE"
PARSED_TEMPLATE="PARSED_TEMPLATE"


space = []

g = {X:0, Y:0, CLIPX:0, CLIPY:0, CLIPX1: None, CLIPY1: None,
     TEMPLATE: None, PARSED_TEMPLATE: None}

S = []


def push(obj): S.append(obj)
def pop(): return S.pop()

def pushpos(): push((g[X], g[Y]))
def poppos(): g[X], g[Y] = pop()

def pushclip(): push((g[CLIPX], g[CLIPY], g[CLIPX1], g[CLIPY1]))
def popclip(): g[CLIPX], g[CLIPY], g[CLIPX1], g[CLIPY1] = pop()

def pushspace(): push(copy.deepcopy(space))
def popspace(): space[:] = copy.deepcopy(pop())


def loc(x=None,y=None):
    if x is None and y is None:
        return (g[X], g[Y])
    elif x is not None and y is not None:
        g[X], g[Y] = x,y
    else:
        raise ValueError()

def clip(x=None, y=None, x1=None, y1=None):
    if x is None and y is None and x1 is None and y1 is None:
        return (g[CLIPX], g[CLIPY], g[CLIPX1], g[CLIPY1])
    elif x is not None and y is not None and x1 is not None and y1 is not None:
        g[CLIPX], g[CLIPY], g[CLIPX1], g[CLIPY1] = x,y,x1,y1
    else:
        raise ValueError()

def clipwh():
    return (g[CLIPX], g[CLIPY], g[CLIPX1]-g[CLIPX], g[CLIPY1]-g[CLIPY])


def inspace(x,y):
    """Check if space contains a coordinate."""
    return not (y >= len(space) or x >= len(space[y]))

def xspace(x,y):
    """Extend space to contain a coordinate."""
    if y >= len(space):
        space.extend([[] for i in range(y+1-len(space))])
    ln = space[y]
    if x >= len(ln):
        ln.extend([" " for i in range(x+1-len(ln))])

def dims():
    return (max([len(row) for row in space]), len(space))


def peek(x,y):
    return space[y][x] if inspace(x,y) else None

def poke(x,y, ch):
    """poke a single character to an x,y position"""
    if g[CLIPX] is not None and x < g[CLIPX]: return
    if g[CLIPX1] is not None and x >= g[CLIPX1]: return
    if g[CLIPY] is not None and y < g[CLIPY]: return
    if g[CLIPY1] is not None and y >= g[CLIPY1]: return
    xspace(x,y)
    space[y][x] = ch


def readrow(x,x1,y, default=""):
    L = []
    for i in range(x,x1):
        L.append(peek(i,y) or default)
    return "".join(L)

def readcol(x,y,y1, default=""):
    L = []
    for i in range(y,y1):
        L.append(peek(x,i) or default)
    return "".join(L)

def writerow(x,x1,y, s):
    si = 0
    for i in range(x,x1):
        poke(i,y, s[si])
        si += 1

def writecol(x,y,y1, s):
    si = 0
    for i in range(y,y1):
        poke(x,i, s[si])
        si += 1


def clear():
    space[:] = []
    g[X] = 0
    g[Y] = 0

def clip0():
    g[CLIPX] = 0
    g[CLIPY] = 0
    g[CLIPX1] = None
    g[CLIPY1] = None

def reset():
    space[:] = []
    g[X] = 0
    g[Y] = 0
    g[CLIPX] = 0
    g[CLIPY] = 0
    g[CLIPX1] = None
    g[CLIPY1] = None
    g[TEMPLATE] = None
    g[PARSED_TEMPLATE] = None


def chart(flags=""):
    """
    flags:
      e -- show ends ("|") where data storage stops for a row
    """
    if len(space) == 0: return "(empty)"
    show_ends = "e" in flags
    L = ["    0.       10.       20.       30.       40.       50.         ",
         "     0123456789     5    0123456789     5    0123456789     5    ",
         "    \\O....o....O....o....O....o....O....o....O....o....O....o...."]  # 4+60.
    for (i,ln) in enumerate(space):
        ch = "O" if i % 5 == 0 else "."
        end = "|" if show_ends else ""
        L.append("{:>3} {}{}{}".format(i, ch, "".join(ln)[:60], end))
    return "\n".join(L)

def show():
    print(chart())


def as_str():
    return "\n".join(["".join(L) for L in space])


def write(s, flags="f"):
    """
    flags:
      "o" -- "Stay at original position" -- cursor not moved
      "e" -- "Stay at end" -- cursor left at final cursor pos
      "h" -- "Home at end" -- cursor left at initial X in last row pos
                              [useful if ending w/ training newline]
      "f" -- "Follow" -- cursor left at line at initial X in following row pos
    """
    x,y = g[X], g[Y]
    for ch in s:
        if ch == "\n":
            x = g[X]
            y += 1
        else:
            poke(x,y,ch)
            x += 1
    if "o" in flags:  # keep cursor at original position
        pass
    elif "e" in flags:  # keep cursor at last position
        g[X], g[Y] = x, y
    elif "h" in flags:  # cursor left at start of last row
        g[Y] = y  # this can be useful when ending with a trailing newline
    elif "f" in flags:  # cursor follows in a new row
        g[Y] = y+1  # cursor moved to last y position, plus 1; left side remains same


# primitive drawing

def hline(x,x1,y,ch):
    "x1 is exclusive"
    for i in range(x,x1):
        poke(i,y,ch)

def vline(x,y,y1,ch):
    "y1 is exclusive"
    for i in range(y,y1):
        poke(x,i,ch)

def box(x,y,x1,y1, ch):
    "x1 and y1 are exclusive"
    hline(x,x1,y,ch)
    hline(x,x1,y1-1,ch)
    vline(x,y,y1,ch)
    vline(x1-1,y,y1,ch)

def fill(x,y,x1,y1, ch):
    "x1 and y1 are exclusive"
    for y in range (y,y1):
        hline(x,x1,y, ch)


def cut(x,y,x1,y1):
    L = []
    for i in range(y,y1):
        L.append(readrow(x,x1,i, default=" "))
        writerow(x,x1,i, " "*len(L[-1]))
    return "\n".join(L)

def copy(x,y,x1,y1):
    L = []
    for i in range(y,y1):
        L.append(readrow(x,x1,i, default=" "))
    return "\n".join(L)

def paste(x,y, s):
    pushpos()
    loc(x,y)
    write(s, "o")
    poppos()


def use_template(template):
    import strscan
    g[TEMPLATE] = template
    g[PARSED_TEMPLATE] = strscan.scan(template)

def copy_template():
    clear()
    write(g[TEMPLATE], "o")

def template_clip(label):
    for (x,x1,y,y1, cur_lbl, kind) in g[PARSED_TEMPLATE]:
        if label == cur_lbl:
            clip(x,y,x1,y1)
            return

def template_write(label, text):
    pushpos()
    pushclip()
    for (x,x1,y,y1, cur_lbl, kind) in g[PARSED_TEMPLATE]:
        if kind in {".", "_"} and label == cur_lbl:
            clip(x,y,x1,y1)
            fill(x,y,x1,y1, " ")
            loc(x,y)
            write(text, "o")
    popclip()
    poppos()

"""
An Example:

from strpaint import *
import strscan
use_template(strscan.test)
copy_template()
template_write("baz", "this is a test")
"""

