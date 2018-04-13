;; This buffer is for text that is not saved, and for Lisp evaluation.
;; To create a file, visit it with C-x C-f and enter text in its buffer.

def plot_skycoords(system='Galactic', axis='latitude',
                   units='degree', wrap_ra24hr=False,
                   overplot=False, label=True):
    """
    could be generalised for ecliptic and lat/long

    based on IDL plot_galcoords.pro
    handles 24hr wrap

    """

    print('Plotting ' + system + ' Coordinates')
    print('plot_skycoords; label:', label)

    if not overplot:
        plt.figure(figsize=(8.0, 6.0))

    if system == 'Galactic':
        color = 'red'
        latitudes = [-30.0, -5.0, 0.0, 5.0, 30.0]
        linestyles = ['--', '--', '-', '--', '--']

        # latitudes= [-30.0, -20.0,-10.0, -5.0, 0.0, 5.0, 10.0, 20.0, 30.0]
        # linestyles = [ '--', '--', '--', '--', '-', '--','--', '--','--']

    if system == 'Ecliptic':
        color = 'blue'
        latitudes = [0.0]
        linestyles = ['-.']

        # latitudes= [-30.0, -20.0,-10.0, -5.0, 0.0, 5.0, 10.0, 20.0, 30.0]
        # linestyles = [ '--', '--', '--', '--', '-', '--','--', '--','--']

    npoints = 3600
    npoints = npoints + 1

    ilabel = 0
    ilat = -1
    # could be generalised for longitude and ecliptic coordinates
    for lat in latitudes:
        ilat = ilat + 1
        print('latitude:', lat, latitudes[ilat])

        latitude = np.full((npoints,), lat)
        longitude = np.linspace(0.0, 360.0, num=npoints)

        if system == 'Galactic':

            Galactic = SkyCoord(
                longitude * u.degree,
                latitude * u.degree, frame='galactic')
            Galactic_icrs = Galactic.icrs

            if wrap_ra24hr:
                ra = Galactic_icrs.ra.wrap_at(180 * u.deg).degree
            if not wrap_ra24hr:
                ra = Galactic_icrs.ra.degree
            dec = Galactic_icrs.dec.degree

        if system == 'Ecliptic':
            Ecliptic = SkyCoord(
                longitude * u.degree,
                latitude * u.degree, frame='geocentrictrueecliptic')
            Ecliptic_icrs = Ecliptic.icrs

            if wrap_ra24hr:
                ra = Ecliptic_icrs.ra.wrap_at(180 * u.deg).degree
            if not wrap_ra24hr:
                ra = Ecliptic_icrs.ra.degree

            dec = Ecliptic_icrs.dec.degree

        print('0,0: ', ra[0], dec[0])

        # determine if where there are 24hrs wraps
        if units == 'degree':
            wrap_range = 240.0
        if units == 'hour':
            wrap_range = 18.0
            ra = ra / 15.0

        i = -1
        nwrap = 0
        iwrap = 0
        wrap = []
        ndata = len(ra)
        for i in range(0, ndata):
            if i <= ndata - 2:
                if abs(ra[i] - ra[i + 1]) >= wrap_range:
                    wrap.append(i)
                    iwrap = iwrap + 1
                    print('wrap:', iwrap, i, ra[i], ra[i + 1])
        nwrap = iwrap

        print('plot_skycoords; label:', label, ilabel)
        if label is not None:
            label = system + ' Coordinates'
        print('plot_skycoords; label:', label, ilabel)

        linestyle = linestyles[ilat]
        if nwrap == 0:
            print('No wrapping: ', latitudes[ilat])

            xdata = ra
            ydata = dec

            ilabel = plot_skycoords_plot(
                xdata, ydata, linestyle=linestyle,
                label=label, ilabel=ilabel, color=color,
                wrap_ra24hr=wrap_ra24hr, units=units)

        if nwrap == 1:
            iwrap = 0
            print()
            print('wrapping:', latitudes[ilat], nwrap)
            print('wrap at: ', wrap)
            print(iwrap, wrap[iwrap], ra[wrap[iwrap]], ra[wrap[iwrap] + 1])
            print(iwrap, wrap[iwrap], dec[wrap[iwrap]], dec[wrap[iwrap] + 1])

            ndata = len(ra)
            xdata = ra[0:wrap[iwrap]]
            ydata = dec[0:wrap[iwrap]]

            ilabel = plot_skycoords_plot(
                xdata, ydata, linestyle=linestyle,
                label=label, ilabel=ilabel, color=color,
                wrap_ra24hr=wrap_ra24hr, units=units)

            xdata = ra[wrap[iwrap] + 1:-1]
            ydata = dec[wrap[iwrap] + 1:-1]

            ilabel = plot_skycoords_plot(
                xdata, ydata, linestyle=linestyle,
                label=label, ilabel=ilabel, color=color,
                wrap_ra24hr=wrap_ra24hr, units=units)

        if nwrap >= 2:
            print()
            print('wrapping: ', latitudes[ilat], nwrap)
            print('wrap at: ', wrap)

            isegment = 0
            for iwrap in range(0, nwrap):
                print()
                print(iwrap, nwrap, wrap[iwrap],
                      ra[wrap[iwrap] - 1], ra[wrap[iwrap]],
                      ra[wrap[iwrap] + 1])
                print(iwrap, nwrap, wrap[iwrap],
                      dec[wrap[iwrap] - 1], dec[wrap[iwrap]],
                      dec[wrap[iwrap] + 1])

                if iwrap == 0:
                    isegment = isegment + 1
                    print()
                    print('segment: ', isegment)
                    print(iwrap, nwrap, 0, '-', wrap[iwrap])
                    print('segment (RA):  ', ra[0], '-', ra[wrap[iwrap]])
                    print('segment (Dec): ', dec[0], '-', dec[wrap[iwrap]])

                    xdata = ra[0:wrap[iwrap]]
                    ydata = dec[0:wrap[iwrap]]

                    ilabel = plot_skycoords_plot(
                        xdata, ydata,
                        linestyle=linestyle, color=color,
                        label=label, ilabel=ilabel,
                        wrap_ra24hr=wrap_ra24hr, units=units)

                if iwrap != 0:
                    isegment = isegment + 1
                    print()
                    print('segment: ', isegment)
                    print(iwrap, nwrap, wrap[iwrap - 1] + 1, '-', wrap[iwrap])
                    print('segment (RA):',
                          ra[wrap[iwrap - 1] + 1], '-', ra[wrap[iwrap]])
                    print('segment (Dec):',
                          dec[wrap[iwrap - 1] + 1], '-', dec[wrap[iwrap]])

                    xdata = ra[wrap[iwrap - 1] + 1:wrap[iwrap]]
                    ydata = dec[wrap[iwrap - 1] + 1:wrap[iwrap]]

                    ilabel = plot_skycoords_plot(
                        xdata, ydata,
                        linestyle=linestyle, color=color,
                        label=label, ilabel=ilabel,
                        wrap_ra24hr=wrap_ra24hr, units=units)

                if iwrap == nwrap - 1:
                    isegment = isegment + 1
                    print()
                    print('segment: ', isegment)
                    print(iwrap, nwrap, wrap[iwrap], npoints - 1)
                    print('segment (RA): ', ra[wrap[iwrap] + 1], '-', ra[-1])
                    print('segment (Dec):', dec[wrap[iwrap] + 1], '-', dec[-1])

                    xdata = ra[wrap[iwrap] + 1:-1]
                    ydata = dec[wrap[iwrap] + 1:-1]

                    ilabel = plot_skycoords_plot(
                        xdata, ydata,
                        linestyle=linestyle, color=color,
                        label=label, ilabel=ilabel,
                        wrap_ra24hr=wrap_ra24hr, units=units)

    plt.legend(fontsize='small')
    plt.grid()
    figname = appname + '_galactic_' + datestamp + '.png'
    print('Saving:' + figname)
    plt.savefig('./' + figname)

    return
