from __future__ import print_function

import sys
import inspect
import traceback

def lineno(functionName=True, fileName=True,
           USEtraceback=False,
           debug=False, verbose=False, info=False):

    """Return current function line number, name and filename

    info and verbose modes are the same

    loosely based on code by Danny Yoo (dyoo@hkn.eecs.berkeley.edu)

    using inspect: see
    http://code.activestate.com/recipes/145297-grabbing-the-current-line-number-easily/

    http://python.org/doc/lib/module-inspect.html

    It can also be done with traceback; see plotid.py

    https://docs.python.org/2/library/traceback.html


    see also http://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback

    Note inspect.stack calls are thousands of times slower than the
    alternatives:

    Also inspect.stack and traceback.extract_stack return
    stack entries in a different order.

    traceback returns a 4-tuple: (filename, line number, function name, text)
    e.g. ('lineno.py', 58, 'lineno', 'stack = traceback.extract_stack()')

    inspect returns a 6-tuple:

     (frame object, filename, line number, function name,
      lines of context from the source code, and
      the index of the current line within that list)

    e.g.

    ( <frame object at 0x100543370>, 'lineno.py', 51, 'lineno',
     ['        stack = inspect.stack()\n'], 0)


    Note:

    You have to return the current level +1 with inspect to get the
    line number information for the calling fucntion i.e.
    [1] for the index
    [0] is this function
    [-1] would be the main.

    Traceback start at the other end so needs
    [-2] for the index to
    the calling function [-] refers to this function.
    [0] would be the main function.



    """


    if debug:

        stack = inspect.stack()
        print()
        print('inspect.stack():', len(stack), len(stack[0]))
        for ilevel, level in enumerate(stack):
            print(ilevel, stack[ilevel])
        print()

        stack = traceback.extract_stack()
        print()
        print('traceback.extract_stack():', len(stack), len(stack[0]))
        for ilevel, level in enumerate(stack):
            print(ilevel, stack[ilevel])
        print()

        print('traceback.extract_stack()[-1][2]:',
              traceback.extract_stack()[-1][2])

        print('inspect.stack()[0][0]:',
              inspect.stack()[0][0])

        print('inspect.stack()[0][3]:',
              inspect.stack()[0][3])

        print('inspect.stack()[0][0].f_code.co_name:',
              inspect.stack()[0][0].f_code.co_name)

        print('inspect.currentframe().f_code.co_name:',
              inspect.currentframe().f_code.co_name)

        print('sys._getframe().f_code.co_name:',
              sys._getframe().f_code.co_name)


    if USEtraceback:
        # (filename, line number, function name*, text)

        lineno = traceback.extract_stack()[-2][1]

        result = lineno

        if functionName:
            functionname = traceback.extract_stack()[-2][2]
            result = (functionname, lineno)

        if fileName:
            filename = traceback.extract_stack()[-2][0]
            result = (lineno, filename)

        if fileName and functionName:
            result = (functionname, lineno, filename)


    if not USEtraceback:
        # (frame object, filename, line number, function name,
        #  lines of context from the source code, and
        #  the index of the current line within that list)

        # lineno = inspect.currentframe().f_back.f_lineno
        lineno = inspect.stack()[1][2]

        result = lineno

        if functionName:
            functionname = inspect.stack()[1][3]
            result = (functionname, lineno)

        if fileName:
            filename = inspect.stack()[1][1]
            result = (lineno, filename)

        if fileName and functionName:
            result = (functionname, lineno, filename)

    if verbose or info:
        print('INFO:', __file__, __name__,
              ' '.join([str(i) for i in result]))

    return result

if __name__ == '__main__':

    print()
    print("Report line number using inspect:\n",
          lineno(debug=True, verbose=True))
    print()
    print()
    print("Report line number using tracback:\n",
          lineno(USEtraceback=True, debug=True, verbose=True))
    print()
    print()
    print("Using inspect:\n")
    lineno(verbose=True)
    print()
    print("Using tracback:\n")
    lineno(USEtraceback=True, verbose=True)
