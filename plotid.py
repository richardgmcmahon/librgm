from __future__ import print_function, division


def plotid(timestamp=True, user=True, hostname=False,
           color='k', backgroundcolor='w',
           weight='ultralight',
           progname=True, label=None, fontsize='small',
           top=False, right=False, verbose=False,
           debug=False, traceback=True,
           githash=True):
    """
    Adds timestamp and other provenance information to a plot.


    Options:
    include date, username, hostname, program filename

    fontsize = ['x-small', 'small']

    could even geotag it?
    could add provenance to the png file

    Considerations:

    should the text location be in units of the current figure (gcf)
    or the current axis (gca)

    see also https://github.com/matplotlib/matplotlib/issues/289

    options are not implemented yet
    text is placed on middle right in axis cords.

    """

    import os
    import time
    import datetime
    import traceback

    import getpass
    import socket

    import subprocess

    import matplotlib.pyplot as plt


    hostname_str = ''
    if hostname:
        hostname_str = socket.gethostname()

    now = time.localtime(time.time())
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", now)

    # print os.path.basename(trace[0]), ' line :', str(trace[1])
    # progname=os.path.basename(__file__)


    if githash:
        provenance = ''
        gitHash = ''
        # put provenance on the side of the plot
        try:
            gitHash = subprocess.check_output(["git", "rev-parse",
                                               "--short", "HEAD"]).strip()
        except subprocess.CalledProcessError as e:
            print("You need to be in a git repository in order to put " +
                  "provenance information on the plots. Please clone the " +
                  "repository instead of downloading the source files " +
                  "directly, and ensure that your local git repo hasn't " +
                  "been corrupted")

        gitHash = gitHash.decode("utf-8")
        try:
            producer = subprocess.check_output(["git", "config",
                                                "user.name"]).strip()
        except subprocess.CalledProcessError as e:
            print("You have not set the git user.name property, which " +
                  "is needed to add provenance information on the plots. " +
                  "You can set this property globally using the command " +
                  "git config --global user.name '<my name>'")

        provenance = producer.decode("utf-8") + ", " + gitHash

    # provenance += "\n Using {} QLF with k={:2.4f}".format(config.qlfName, config.k)
    # plt.figtext(0.93, 0.5, provenance, rotation="vertical",
    #        verticalalignment="center", alpha=0.7)


    if debug:
        trace = traceback.print_exc()
        # help(trace)
        # print('len(trace): ', len(trace))
        trace = traceback.extract_stack()
        # help(trace)
        print('len(trace):', len(trace))
        for each in trace:
            print(each)

    progname_str = ''
    progline = ''
    if progname:
        trace = traceback.extract_stack()[0]
        progname_str = os.path.basename(trace[0])
        progline = str(trace[1])
        progline = '({})'.format(progline)

    if debug:
        print('progname:', progname)
        print('progname_str:', progname_str)
        print('progline:', progline)

    # username=os.environ['USER']
    username = getpass.getuser()

    now = time.localtime(time.time())
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", now)
    if debug or verbose:
        print('timestamp:', timestamp)

    if label is None:
        label = ''

    text = '{} {}{} {} {}'.format(label,
                                     progname_str, progline,
                                     username, timestamp)

    # text = label+ ':  ' +timestamp+ ' ' +username
    # if host: text = text + '@'+hostname+']'

    if debug or verbose:
        print('text:', text)

    # cf plt.text
    # see http://matplotlib.org/users/text_props.html

    # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.figtext
    # http://matplotlib.org/examples/pylab_examples/alignment_test.html
    # http://matplotlib.org/users/transforms_tutorial.html
    # explore difference between text and figtext

    # get current axis (gca)
    # ax=plt.gca()
    transform = plt.gca().transAxes
    # transform=plt.gcf().transFigure

    # this is needed to allow the text to be added before the first
    # axes are drawn
    # plt.setp(plt.gca(), xticks=(), yticks=())#, frame_on=False

    figtext = True
    xtext = 0.98
    dxtext = 0.030
    if figtext:
        plt.figtext(xtext, 0.5,
                    text,
                    transform=transform,
                    rotation=90,
                    size=fontsize, color=color,
                    backgroundcolor='w',
                    fontsize=fontsize,
                    weight='ultralight',
                    horizontalalignment='left',
                    verticalalignment='center')

        cwd = os.getcwd()

        text = '{} {}'.format(cwd, hostname_str)

        xtext = xtext - dxtext
        plt.figtext(xtext, 0.5,
                    text,
                    transform=transform,
                    rotation=90,
                    size=fontsize, color=color,
                    backgroundcolor='w',
                    fontsize=fontsize,
                    weight='ultralight',
                    horizontalalignment='left',
                    verticalalignment='center')

    # give the funtion call info
    if traceback:
        trace = traceback.extract_stack()[1]
        progname_str = os.path.basename(trace[0])
        progline = str(trace[1])
        progline = '({})'.format(progline)
        function_name = trace[2]
        text = '{} {} {} {}'.format(progname_str, progline, function_name,
                                    hostname_str)

        xtext = xtext - dxtext
        plt.figtext(xtext, 0.5,
                    text,
                    transform=transform,
                    rotation=90,
                    size=fontsize, color=color,
                    backgroundcolor='w',
                    fontsize=fontsize,
                    weight='ultralight',
                    horizontalalignment='left',
                    verticalalignment='center')

    if not figtext:
        plt.text(0.97, 0.5,
                 text,
                 transform=transform,
                 rotation=90,
                 size=fontsize, color=color,
                 backgroundcolor='w',
                 fontsize=fontsize,
                 weight='ultralight',
                 horizontalalignment='left',
                 verticalalignment='center')


    if githash:
        xtext = 0.02
        plt.figtext(xtext, 0.5,
                    provenance,
                    transform=transform,
                    rotation=90,
                    size=fontsize, color=color,
                    backgroundcolor='w',
                    fontsize=fontsize,
                    weight='ultralight',
                    horizontalalignment='left',
                    verticalalignment='center')

    return

if __name__ == '__main__':

    import matplotlib.pyplot as plt

    plt.plot(range(10), label='label')

    plt.grid()

    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.title('Title')
    plt.suptitle('Suptitle')
    plt.legend()

    plotid(debug=True, progname=True)

    plt.show()
