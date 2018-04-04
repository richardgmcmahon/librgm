import numpy as np


def moments2ellipse(X2, Y2, XY):
    """
    convert Sextractor 2nd order moments to ellipse parameters

    http://sextractor.readthedocs.io/en/latest/Measurements.html

    """

    A2 = (0.5 * (X2 + Y2)) + \
         np.sqrt(np.power(((X2 - Y2) / 2.0), 2) + np.power(XY, 2))
    a = np.sqrt(A2)

    B2 = (0.5 * (X2 + Y2)) -
    np.sqrt(np.power(((X2 - Y2) / 2.0), 2) + np.power(XY, 2))
    b = np.sqrt(B2)

    # tan(2theta) =
    tan2theta = 2.0 * XY / (X2 - Y2)

    XYsign = np.sign(XY)

    # using arctan2 and not arctan
    theta = np.rad2deg(np.arctan(tan2theta) / 2.0)

    return a, b, theta
