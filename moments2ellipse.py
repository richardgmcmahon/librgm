import numpy as np


def moments2ellipse(X2, Y2, XY, XYsigntest=True):
    """
    convert Sextractor 2nd order moments to ellipse parameters

    X2 == XX
    Y2 == YY

    Options: XYsigntest=True is needed to deal with the theta degeneracy

    See http://sextractor.readthedocs.io/en/latest/Measurements.html


    Over the domain THETA has two different angles with opposite signs.
    THETA is the solution to (7) that has the same sign as the covariance
    XY.

    Returns: a (pixels), b (pixels), theta (degrees)

    """

    A2 = (0.5 * (X2 + Y2)) + \
         np.sqrt(np.power(((X2 - Y2) / 2.0), 2) + np.power(XY, 2))
    a = np.sqrt(A2)

    B2 = (0.5 * (X2 + Y2)) - \
    np.sqrt(np.power(((X2 - Y2) / 2.0), 2) + np.power(XY, 2))
    b = np.sqrt(B2)

    # tan(2theta) =
    tan2theta = 2.0 * XY / (X2 - Y2)

    # deal with the quadrant degeneracy
    XYsign = np.sign(XY)
    print(type(XYsign), len(XYsign))
    help(XYsign)

    # using arctan2 and not arctan
    theta = np.rad2deg(np.arctan(tan2theta) / 2.0)

    if XYsigntest:
        itest = (XYsign == +1) & (theta < 0.0)
        theta[itest] = theta[itest] + 90.0

        itest = (XYsign == -1) & (theta > 0.0)
        theta[itest] = theta[itest] - 90.0

    return a, b, theta
