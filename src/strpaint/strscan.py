"""strscan  -- String Scanner

Scans a string like:

  ..foo..............................  This is a literal string
  ...................................
  ...................................  ...bar...............................
  ...................................  .....................................
  ...................................  .....................................

  __baz__________
  __boz__________

...and outputs regions:

  x, x1, y, y1                      -- x1, y1 exclusive
[(2, 37, 1, 6, 'foo', '.'),
 (39, 43, 1, 2, 'This', 'LIT'),
 (44, 46, 1, 2, 'is', 'LIT'),
 (47, 48, 1, 2, 'a', 'LIT'),
 (49, 56, 1, 2, 'literal', 'LIT'),
 (57, 63, 1, 2, 'string', 'LIT'),
 (39, 76, 3, 6, 'bar', '.'),
 (2, 17, 7, 8, 'baz', '_'),
 (2, 17, 8, 9, 'boz', '_')]

Each of those lines has the form:

  (x0, x1-exclusive,
   y0, y1-exclusive,
   label string (or None),
   "LIT" "_" or ".")

"_" lines are considered x1 per line;
"." lines aggregate across rectangular regions
"""


labelchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def scanline(s):
    i = 0  # start @ beginning of line
    R = []  # (t, x0,x1, lbl)  t:./_/LIT  lbl:label/None
    def read(sym):  # "." or "_" -- called 'dots' now
        j = i  # local traverser
        while j < len(s) and s[j] == sym:
            j += 1  # eat leading dots
        if j < len(s) and s[j] in labelchars:
            m = j  # mark label start
            while j < len(s) and s[j] in labelchars:
                j += 1  # eat label characters
            label = s[m:j]
            if j < len(s) and s[j] == sym:
                while j < len(s) and s[j] == sym:
                    j += 1  # eat any trailing dots
            R.append((sym, i, j, label))
        else:
            R.append((sym, i, j, None))
    while i < len(s):
        if s[i] in "._":
            read(s[i])
            i = R[-1][2]  # last pos
        else:
            i += 1
    return R


def scan(s):
    lnno = 0
    R = []  # (x0,x1-exclu, y0,y1-excl, lbl, t)
    active = set()
    for ln in s.splitlines():
        for (t, x0,x1, lbl) in scanline(ln):
            if t == "_" or t == "LIT":
                R.append((x0,x1,lnno,lnno+1,lbl,t))
            else:
                for i in active:
                    if R[i][0] == x0 and R[i][1] == x1:
                        x0,x1,y0,y1,lbl,t = R[i]
                        R[i] = (x0,x1,y0,lnno+1,lbl,t)
                        break
                else:
                    R.append((x0,x1,lnno,lnno+1,lbl,t))
                    active.add(len(R)-1)
        active.difference_update([i for i in active if R[i][3] != lnno+1])
        lnno += 1
    return R


test = """

  ..foo..............................  This is a literal string
  ...................................
  ...................................  ...bar...............................
  ...................................  .....................................
  ...................................  .....................................

  __baz__________
  __boz__________


"""[1:-1]


