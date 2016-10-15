"""
A cubic bezier curve is defined in terms of a parameter t as:

B(t) = (1-t)^3 A + 3t(1-t)^2 B + 3t^2(1-t) C + t^3 D for 0 <= t <= 1 

"""

import numpy as np
def fit(points):
    size = points.shape[0]
    
    y0 = points[0]
    y1 = points[int(size/3)]
    y2 = points[int(2*size/3)]
    y3 = points[size-1]

    # https://web.archive.org/web/20131225210855/http://people.sc.fsu.edu/~jburkardt/html/bezier_interpolation.html
    p0 = y0
    p1 = ((-5)*y0 + 18*y1 - 9*y2 + 2*y3) / 6
    p2 = (2*y0 - 9*y1 + 18*y2 - 5*y3) / 6
    p3 = y3

    return np.array([p0, p1, p2, p3])

GRANULARITY = 500
def generate_points(curve_parameters):
    t = np.linspace(0, 1, num=GRANULARITY)
    coeffs = np.array([(1 - t)**3, 3*t*((1-t)**2), 3*(t**2)*(1-t), t**3])
    coeffs = np.transpose(coeffs)
    control_points = np.tile(curve_parameters, (t.shape[0], 1, 1))
    x_points = control_points[:,:,0]
    y_points = control_points[:,:,1]
    x_coords = np.sum(np.multiply(coeffs, x_points), axis=1)
    y_coords = np.sum(np.multiply(coeffs, y_points), axis=1)

    return np.transpose(np.array([x_coords, y_coords]))

"""

Old code, attempting to solve entire interpolation problem with generic solver

import numpy as np
import functools
import scipy.optimize

GRANULARITY = 500


def fit(points):
    data = np.copy(points)

    min_x = min(points[:,0])
    min_y = min(points[:,1])
    max_x = max(points[:,0])
    max_y = max(points[:,1])

    initial_guess = [min_x, max_y,
                     max_x, min_y]
            
    bounds = [(min_x, min_x), (min_y, min_y),
              (-min_x, max_x*2), (-min_y, max_y*2),
              (-min_x, max_x*2), (-min_y, max_y*2),
              (max_x, max_x), (max_y, max_y)]

    v_range = max(max_x - min_x, max_y - min_y)*4
    
    def cb(x):
        print(err_func(x))

    def err_func(x):
        curve_params = [min_x, min_y, x[0], x[1], x[2], x[3], max_x, max_y]
        return __bezier_error(points, curve_params)

                         
    result = scipy.optimize.basinhopping(err_func, initial_guess, niter=200, T=v_range, disp=True)
    #result = scipy.optimize.differential_evolution(err_func, bounds, disp=True)
    x = result.x
    curve_params = [min_x, min_y, x[0], x[1], x[2], x[3], max_x, max_y]

    print("Objective function final value: " + str(result.fun))
    return np.reshape(curve_params, (4, 2))
                     
def generate_points(curve_parameters):
    t = np.linspace(0, 1, num=GRANULARITY)
    coeffs = np.array([(1 - t)**3, 3*t*((1-t)**2), 3*(t**2)*(1-t), t**3])
    coeffs = np.transpose(coeffs)
    control_points = np.tile(curve_parameters, (t.shape[0], 1, 1))
    x_points = control_points[:,:,0]
    y_points = control_points[:,:,1]
    x_coords = np.sum(np.multiply(coeffs, x_points), axis=1)
    y_coords = np.sum(np.multiply(coeffs, y_points), axis=1)

    return np.transpose(np.array([x_coords, y_coords]))


def __bezier_error(points, curve_parameters):
    curve_parameters = np.reshape(np.array(curve_parameters), (4, 2))

    points_on_curve = np.transpose(generate_points(curve_parameters))
    x_coords = points_on_curve[0]
    y_coords = points_on_curve[1]
    
    closest_x = [np.searchsorted(x_coords, x) for x in points[:,0]]
    y_values = np.array([y_coords[x] if x < GRANULARITY else y_coords[GRANULARITY-1] for x in closest_x])
    y_value_diffs = (y_values - points[:,1])**2
    return sum(y_value_diffs)
    
"""

if __name__ == "__main__":
    print(fit(np.array([[153, 900],
                        [154, 1200],
                        [156, 1400],
                        [167, 1000],
                        [178, 800],
                        [190, 300]])))
    
    
