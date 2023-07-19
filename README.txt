title: strpaint -- readme.md
date: 2021-07-01


== Welcome ==
date: 2021-07-01

  Project Title: 2-Dimensional String Painting
  Project Summary: 2-dimensional string painter

  This is an imperative system for painting 2-D outputs.  You can think
  of it as being a "Turtle"-like system, for composing outputs for
  print(...) commands.

  Here's an example:

----------------------------------------------------------------------
import strpaint

strpaint.loc(5,5)
strpaint.write("This is a test.")
strpaint.write("It is ONLY a test.")
strpaint.write("In the event of an actual emergency, ...")
s = strpaint.as_str()
----------------------------------------------------------------------

  The value of "s" is now:

    '\n'
    '\n'
    '\n'
    '\n'
    '\n'
    '     This is a test.\n'
    '     It is ONLY a test.\n'
    '     In the event of an actual emergency, ...'


  You could continue to draw on the output:

----------------------------------------------------------------------
strpaint.loc(20,2)
strpaint.write("*")
strpaint.loc(34,1)
strpaint.write("*")
strpaint.loc(27,4)
strpaint.write("*")
----------------------------------------------------------------------

  Now strpaint.as_str() returns:


    '\n'
    '                                  *\n'
    '                    *\n'
    '\n'
    '                           *\n'
    '     This is a test.\n'
    '     It is ONLY a test.\n'
    '     In the event of an actual emergency, ...'

  If you wanted to confirm the locations, there's a "chart" function
  that shows the output like so:

----------------------------------------------------------------------
     0123456789     5    0123456789     5    0123456789     5
    \O....o....O....o....O....o....O....o....O....o....O....o....
  0 O
  1 .                                  *
  2 .                    *
  3 .
  4 .                           *
  5 O     This is a test.
  6 .     It is ONLY a test.
  7 .     In the event of an actual emergency, ...
----------------------------------------------------------------------


  That should give you the gist of what this code is about.

  It includes functions for:
  
  * clipping -- you can set clipping regions, that nothing will be drawn
                outside of.

  * copying & pasting -- copy & past from & to rectangular regions

  * drawing points, horizontal lines, vertical lines, and boxes

  * transfering and writing to templates


  One last thing, because it's very important:

----------------------------------------------------------------------
strpaint.reset()
----------------------------------------------------------------------

  That's how you wipe the slate clean.

  You can also call "strpaint.clear()", which blanks the image, but
  preserves things like the clipping region, the cursor location, etc.,.

  If you want to recall a previous drawing, ...

----------------------------------------------------------------------
import strpaint

# ... do a bunch of things, drawing to the slate, ...

saved_slate = strpaint.as_str()
strpaint.reset()

# ... now draw a new picture on the slate, ...

second_saved_slate = strpaint.as_str()
strpaint.reset()

# This next command will restore the original slate's contents:

strpaint.write(saved_slate)
----------------------------------------------------------------------

  That should be enough to get you going with this.

