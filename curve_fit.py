import numpy as np
import numpy.polynomial.polynomial as poly
from scipy.optimize import curve_fit


def straight_line_equation(t, a, b):
    return a*t + b


def sigmoid_curve_equation(t, a, b, c):
    return a/(1 + np.exp(-t/b)) + c


def logit_curve_equation(t, a, b, c, d):
    return a*(np.log(b*t / (1 - t/c))) + d


def logarithmic_curve_equation(t, a, b, c):
    return a*np.log(t*b)+c


def exponential_curve_equation(t, a, b):
    return a*np.power((1+b), t)


def exponential_decay_curve_equation(t, a, b):
    return a*np.power((1-b), t)


def logarithmic_decay_curve_equation(t, a, b):
    return a*np.log(t)+b


def generic_curve_equation(t, a, b, c, d, e):
    return a*np.exp(-t/b) + c*np.exp(-t/d) + e


def polynomial_cubic(x, d, c, b, a):
    return a*x*x*x+b*x*x+c*x+d


def straight_line_equation_(a, b):
    return '{}*x + {}'.format(a, b)


def sigmoid_curve_equation_(a, b, c):
    return '{}/(1+e^(-x/{})) + {}'.format(a, b, c)


def logit_curve_equation_(a, b, c, d):
    return '{}*log({}*x/(1-x/{})) + {}'.format(a, b, c, d)


def logarithmic_curve_equation_(a, b, c):
    return '{}*log({}*x) + {}'.format(a, b, c)


def exponential_curve_equation_(a, b):
    return '{}*(1+{})^x'.format(a, b)


def exponential_decay_curve_equation_(a, b):
    return '{}*(1-{})^x'.format(a, b)


def logarithmic_decay_curve_equation_(a, b):
    return '{}*log(x)+{}'.format(a, b)


def generic_curve_equation_(a, b, c, d, e):
    return '{}*e^(-x/{}) + {}*e^(-x/{}) + {}'.format(a, b, c, d, e)


def polynomial_cubic_(a, b, c, d):
    return '{}*x^3+{}*x^2+{}*x+{}'.format(d, c, b, a)


FUNCTIONS = {
    1: ('Straight Line', straight_line_equation, straight_line_equation_),
    2: ('Sigmoid Curve', sigmoid_curve_equation, sigmoid_curve_equation_),
    3: ('Logit Curve', logit_curve_equation, logit_curve_equation_),
    4: ('Logarithmic Curve', logarithmic_curve_equation, logarithmic_curve_equation_),
    5: ('Exponential Curve', exponential_curve_equation, exponential_curve_equation_),
    6: ('Exponential Decay Curve', exponential_decay_curve_equation, exponential_decay_curve_equation_),
    7: ('Log Decay Curve', logarithmic_decay_curve_equation, logarithmic_decay_curve_equation_),
    8: ('Polynomial', polynomial_cubic, polynomial_cubic_),
}


def fit_data(x, y, curve_type=1):
    _, obj, equation = FUNCTIONS[curve_type]
    x_line = np.array(x)

    # Polynomial fitting used polyfit instead of curve_fit from scipy
    if curve_type == 8:
        try:
            popt = poly.polyfit(x, y, 3)
        except:
            popt = poly.polyfit(x, y, 3)

        func = poly.Polynomial(popt)
        y_line = func(x_line)
    else:
        try:
            popt, *_ = curve_fit(obj, x, y)
        except:
            print('Unable to fit curve')
            return
        y_line = obj(x, *popt)
    popt = np.round(popt, 5)
    return x_line, y_line, equation(*popt), popt
