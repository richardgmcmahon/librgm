from __future__ import print_function
"""This provides a lineno() function to make it easy to grab the line
number that we're on.


using inspect: see
http://code.activestate.com/recipes/145297-grabbing-the-current-line-number-easily/


Danny Yoo (dyoo@hkn.eecs.berkeley.edu)

http://python.org/doc/lib/module-inspect.html


It can also be done with traceback; see plotid.py

see also http://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
Note inspect.stack calls are thousands of times slower than the alternatives:


"""
import sys
import inspect
import traceback

def lineno(USEtraceback=False, functionName=True, fileName=True,
           debug=False):
    """Returns the current line number in our program."""

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

        print('inspect.stack()[1][0]):function:',
              inspect.stack()[1][0])
        print('inspect.stack()[1][1]):function:',
              inspect.stack()[1][1])
        print('inspect.stack()[1][2]):function:',
              inspect.stack()[1][2])
        print('inspect.stack()[1][3]):function:',
              inspect.stack()[1][3])

        print('inspect.stack()[0][0].f_code.co_name:function',
              inspect.stack()[0][0].f_code.co_name)

        print('inspect.currentframe().f_code.co_name:function:',
              inspect.currentframe().f_code.co_name)

        print('sys._getframe().f_code.co_name:function:',
              sys._getframe().f_code.co_name)

    if USEtraceback:
        lineno = traceback.extract_stack()[0][1]

    if not USEtraceback:
        lineno = inspect.currentframe().f_back.f_lineno

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

    return result

if __name__ == '__main__':

    print("hello, this is line number using inspect", lineno())
    print()
    print("and now use tracback; this is line", lineno(USEtraceback=True))
