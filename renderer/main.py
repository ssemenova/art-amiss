import scipy.ndimage
import scipy.stats
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import skimage.measure
import itertools
from collections import defaultdict

#import bezier_fit

from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model



def get_color_clusters(img, n):
    # build the training set of all the (r,g,b) pairs
    X = img.reshape(img.shape[0] * img.shape[1], 3)
    kmeans = KMeans(n_clusters=n).fit(X)
    labels = np.array(kmeans.predict(X)).reshape(img.shape[0], img.shape[1])
    labels = scipy.ndimage.filters.median_filter(labels, size=(5,5))
    return kmeans.cluster_centers_, labels

def get_contours(img, n):
    # the results from find_contour are (row, column) pairs, which is (y, x).
    # we want x, y
    contours = itertools.chain.from_iterable(skimage.measure.find_contours(img, x) for x in range(n))
    flipped_contours = (np.array(x[:,[1, 0]]) for x in contours)
    rounded = (x.astype(np.int32) for x in flipped_contours)
    return np.array(list(itertools.chain.from_iterable(rounded)))

def group_points_by_row(points, num_rows):
    # group all the points based on their y coord (row), and then sort each row by the x coord
    toR = defaultdict(list)
    for p in points:
        toR[p[1]].append(p[0])

    toR = {k: list(remove_adajcent_values(sorted(v))) for k,v in toR.items()}

    max_pts = max(len(x) for _,x in toR.items())
    toR = {k: v for k, v in toR.items() if len(v) == max_pts}
    toR = [[(x, y) for x in xlist] for y,xlist in toR.items()]
    
    return np.transpose(np.array(toR), (1, 0, 2))


def remove_adajcent_values(values, error=2):
    last = None
    for x in values:
        if last != None and abs(last - x) < error:
            last = x
            continue
        last = x
        yield x

def fit_polynomials(row_points, k=4):
    curve_parameters = []
    for contour in row_points:
        values = contour[:,1]
        lbls = contour[:,0]
        curve_parameters.append(np.poly1d(np.polyfit(values, lbls, k)))
    return curve_parameters

def create_contour_points(polys, num_rows):
    contours = []
    for bcurve in polys:
        y = np.arange(0, num_rows)
        x = bcurve(y)
        pts = np.transpose(np.array([x, y])).astype(np.int32)
        contours.append(pts)
    return sorted(contours, key=lambda x: x[0][0])

def neighbors(point, shape):
    toR = []
    if point[0] - 1 >= 0: toR.append([point[0] - 1, point[1]])
    if point[1] - 1 >= 0: toR.append([point[0], point[1] - 1])
    if point[0] + 1 < shape[0]: toR.append([point[0] + 1, point[1]])
    if point[1] + 1 < shape[1]: toR.append([point[0], point[1] + 1])

    return toR
    
def expand_region(labels, start, to_label):
    # starting at the start point, expand the region until
    # we hit something that is not zero. Label everything in this region
    # with to_label
    queue = [start]
    while len(queue) != 0:
        nxt = queue.pop()
        if labels[nxt[0], nxt[1]] == 0:
            labels[nxt[0], nxt[1]] = to_label
            queue.extend(neighbors(nxt, labels.shape))
    return labels
        

def get_regions(img_dim, contours):
    # for the given set of contour points, produce a 2D matrix with dimension
    # img_dim with each region labelled with a different integer.

    labels = np.zeros(img_dim)

    # put in all of our contours as -1s
    for contour in contours:
        idx = np.transpose(contour)[[1,0]]
        labels[idx[0], idx[1]] = -1

    current_label = 1
    while True:
        # find the first unlabeled point
        unlabeled = np.transpose(np.where(labels == 0))

        if len(unlabeled) == 0:
            # we have labeled all the points!
            break

        labels = expand_region(labels, unlabeled[0], current_label)
        current_label += 1
    
    return labels, current_label - 1

def get_color_for_label(kmeans_labels, region_labels, label):
    # get the mode of the kmeans label for the region label
    region = np.where(region_labels == label)
    return scipy.stats.mode(kmeans_labels[region]).mode[0]


def interpolate_negative_colors(img):
    # for any color which is negative, set it equal to the average of it's left and right neighbors
    bad_pixels = np.array(np.where(img == -1)[0:2])
    bad_pixels = np.transpose(bad_pixels)
    for p in bad_pixels:
        img[p[0],p[1]] = (img[p[0],p[1]-1] + img[p[0],p[1]+1]) / 2.0
#    img[bad_pixels] = (img[bad_pixels - 1] + img[bad_pixels + 1])/2.0
    return img

img = scipy.ndimage.imread("feitelson.jpg", mode="RGB").astype("float32")

centers, labels = get_color_clusters(img, 3)

#plt.imshow(labels)
#plt.show()

contour = get_contours(labels, 3)

#plt.imshow(labels)
#plt.plot(contour[:,0], contour[:,1], 'w.')
#plt.show()

row_points = group_points_by_row(contour, labels.shape[0])

#plt.imshow(labels)
#plt.plot(row_points[0,:,0], row_points[0,:,1], 'w.')
#plt.plot(row_points[1,:,0], row_points[1,:,1], 'k.')
#plt.plot(row_points[2,:,0], row_points[2,:,1], 'w.')
#plt.plot(row_points[3,:,0], row_points[3,:,1], 'k.')
#plt.plot(row_points[4,:,0], row_points[4,:,1], 'w.')
#plt.plot(row_points[5,:,0], row_points[5,:,1], 'k.')
#plt.show()

region_counts = []
for i in range(2, 10):
    # fit polynomials to each contour line
    curve_parameters = fit_polynomials(row_points, k=i)


    # create an array of points for each contour
    contours = create_contour_points(curve_parameters, labels.shape[0])

    region_labels, num_labels = get_regions(labels.shape, contours)
    print("degree", i, "gives", num_labels)
    region_counts.append(num_labels)

best_k = np.argmin(region_counts) + 2
print("Best K:", best_k)

# fit polynomials to each contour line
curve_parameters = fit_polynomials(row_points, k=best_k)

# create an array of points for each contour
contours = create_contour_points(curve_parameters, labels.shape[0])

#plt.imshow(labels, cmap="hot") 
#for pts in contours:
#    plt.plot(pts[:,0], pts[:,1], 'b')
#plt.show()

region_labels, num_labels = get_regions(labels.shape, contours)

#plt.imshow(region_labels)
#plt.show()


reconstructed_image = np.zeros((labels.shape[0], labels.shape[1], 3))
reconstructed_image.fill(-1)
# find the mode (most common) color within each contour region
for region_label in range(1, num_labels+1):
    color_for_label = centers[get_color_for_label(labels, region_labels, region_label)]
    print(region_label, color_for_label)
    reconstructed_image[np.where(region_labels == region_label)] = color_for_label

reconstructed_image = reconstructed_image.astype(np.int32)
reconstructed_image = interpolate_negative_colors(reconstructed_image)

reconstructed_image = reconstructed_image.astype(np.uint8)

scipy.misc.imsave("model.png", reconstructed_image)

# let's dump the coeffs of the polynomials and the color labels
print(reconstructed_image.shape[0:2])
for curve in curve_parameters:
    print(curve.c)

#plt.imshow(reconstructed_image)
#plt.show()


