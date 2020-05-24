from __future__ import print_function, division


def plotid(timestamp=True, user=True, hostname=False,
           color='k', backgroundcolor='w',
           weight='ultralight',
           progname=True, label=None, fontsize='small',
           top=False, right=False, verbose=False,
           debug=False, traceback=True,
           githash=True, figtext=True):
    """Adds timestamp and other provenance information to a plot

    test:
    python plotid.py makes some demo plots based on Matplotlib examples


    there are at least 3 functions that add text; we use figtext here
    pyplot.text()
    pyplot.figtext()
    pyplot.annotate()


    Options:
    include date, username, hostname, program filename

    fontsize = ['x-small', 'small']

    could even geotag it?
    could add provenance to the png file

    Considerations:

    should the text location be in units of the current figure (gcf)
    or the current axis (gca)

    gcf should like the best

    gcf().transFigure worked for Python 2 but breaks in Python 3
    gca().transAxes works for both Python 2 and 3

    see also https://github.com/matplotlib/matplotlib/issues/289

    some options are not implemented yet
    text is placed on middle right in axis coords.

    """

    import os
    import sys
    import time
    import datetime
    import traceback

    import getpass
    import socket

    import subprocess

    import matplotlib
    import matplotlib.pyplot as plt

    if debug:
        import matplotlib
        print('matplotlib.__version__', matplotlib.__version__)

    hostname_str = ''
    if hostname:
        try:
            hostname_str = socket.gethostname()
            host_ip = socket.gethostbyname(hostname_str)
            print("Hostname :  ",hostname_str)
            print("IP : ",host_ip)
        except:
            print("Unable to get Hostname and IP")


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
        print('pyplot.text:', text)

    # cf plt.text
    # see http://matplotlib.org/users/text_props.html

    # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.figtext
    # http://matplotlib.org/examples/pylab_examples/alignment_test.html
    # http://matplotlib.org/users/transforms_tutorial.html
    # explore difference between text and figtext

    # get current axis (gca)
    # ax=plt.gca()

    # gca().transAxes works for both Python 2 and 3
    # transform = plt.gca().transAxes
    # gca().transAxes works for Python 2
    transform = plt.gcf().transFigure
    if debug:
        # help(transform)
        print('transform:', transform)


    # this is needed to allow the text to be added before the first
    # axes are drawn
    # plt.setp(plt.gca(), xticks=(), yticks=())#, frame_on=False

    xtext = 0.98
    ytext = 0.5
    dxtext = 0.030
    if figtext:
        if debug:
            print('pyplot.figtext:', xtext, ytext, text)
        plt.figtext(xtext, ytext,
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
        if debug:
            print('pyplot.figtext:', xtext, ytext, text)
        plt.figtext(xtext, ytext,
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
        ytext = 0.5
        if debug:
            print('pyplot.figtext:', xtext, ytext, text)
        plt.figtext(xtext, ytext,
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
        xtext = 0.97
        ytext = 0.50
        if debug:
            print('pyplot.text:', xtext, ytext, text)
        plt.text(xtext, ytext,
                 text,
                 transform=transform,
                 rotation=90,
                 size=fontsize, color=color,
                 backgroundcolor='w',
                 fontsize=fontsize,
                 weight='ultralight',
                 horizontalalignment='left',
                 verticalalignment='center')


    # add the Matplotlib and Python version to provenance string
    pythonVersion = 'Python ' + \
                     str(sys.version_info[0]) + '.' + \
                     str(sys.version_info[1]) + '.' + \
                     str(sys.version_info[2]) + '.' + \
                     str(sys.version_info[3])
    matplotlibVersion = 'Matplotlib ' + str(matplotlib.__version__)
    provenance = pythonVersion + '  ' + matplotlibVersion + \
                 '  gitHash: ' + provenance
    if githash:
        text = provenance
        xtext = 0.5
        ytext = 0.97
        if debug:
            print('pyplot.text:', xtext, ytext, text)
        plt.figtext(xtext, ytext,
                    text,
                    transform=transform,
                    rotation=0,
                    size=fontsize, color=color,
                    backgroundcolor='w',
                    fontsize=fontsize,
                    weight='ultralight',
                    horizontalalignment='center',
                    verticalalignment='bottom')

    return

if __name__ == '__main__':

    import sys

    import matplotlib.pyplot as plt

    print(sys.version)
    print(sys.version_info)

    print(range(10))
    plt.plot(range(10), range(10), label='label')

    plt.grid()

    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.title('Title')
    plt.suptitle('Suptitle')
    plt.legend()
    plotid(debug=True, progname=True)

    plotfile = 'plotid_demo_fig1.png'
    print('Saving', plotfile)
    plt.savefig(plotfile)
    plt.show()


    # subplots example
    import numpy as np

    # Some example data to display
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(x, y)
    axs[0, 0].set_title('Axis [0,0]')
    axs[0, 1].plot(x, y, 'tab:orange')
    axs[0, 1].set_title('Axis [0,1]')
    axs[1, 0].plot(x, -y, 'tab:green')
    axs[1, 0].set_title('Axis [1,0]')
    axs[1, 1].plot(x, -y, 'tab:red')
    axs[1, 1].set_title('Axis [1,1]')

    for ax in axs.flat:
       ax.set(xlabel='x-label', ylabel='y-label')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    fig.suptitle('subplot example')
    plotid(debug=True, progname=True)

    plotfile = 'plotid_demo_fig2.png'
    print('Saving', plotfile)
    plt.savefig(plotfile)
    plt.show()

    # subplot example
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    x = np.random.rand(10)
    y = np.random.rand(10)
    z = np.sqrt(x**2 + y**2)

    plt.subplot(321)
    plt.scatter(x, y, s=80, c=z, marker=">")

    plt.subplot(322)
    plt.scatter(x, y, s=80, c=z, marker=(5, 0))

    verts = np.array([[-1, -1], [1, -1], [1, 1], [-1, -1]])
    plt.subplot(323)
    plt.scatter(x, y, s=80, c=z, marker=verts)

    plt.subplot(324)
    plt.scatter(x, y, s=80, c=z, marker=(5, 1))

    plt.subplot(325)
    plt.scatter(x, y, s=80, c=z, marker='+')

    plt.subplot(326)
    plt.scatter(x, y, s=80, c=z, marker=(5, 2))


    plt.suptitle('subplot example')
    plotid()

    plotfile = 'plotid_demo_fig3.png'
    print('Saving', plotfile)
    plt.savefig(plotfile)
    plt.show()


    fig, ax = plt.subplots()

    ax.plot(range(10), range(10), label='label')
    ax.grid()
    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')
    ax.set_title('Title')
    plt.suptitle('Suptitle')
    ax.legend()
    plotid(debug=True, progname=True)

    plotfile = 'plotid_demo_fig4.png'
    print('Saving', plotfile)
    plt.savefig(plotfile)
    plt.show()
