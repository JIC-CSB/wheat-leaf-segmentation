"""Module containing image transformations."""

import numpy as np
import scipy.ndimage.interpolation

from jicbioimage.core.transform import transformation

from jicbioimage.core.util.array import dtype_contract
import skimage.morphology
import skimage.exposure

@transformation
@dtype_contract(input_dtype=bool, output_dtype=bool)
def invert_binary(image):
    """Return an inverted image."""
    return np.logical_not(image)

@transformation
@dtype_contract(input_dtype=bool, output_dtype=bool)
def erosion_binary(image, selem=None):
    return skimage.morphology.binary_erosion(image, selem)

@transformation
@dtype_contract(input_dtype=bool, output_dtype=bool)
def dilation_binary(image, selem=None):
    return skimage.morphology.binary_dilation(image, selem)

@transformation
def equalize(image, nbins=256, mask=None):
    return skimage.exposure.equalize_hist(image, nbins=nbins, mask=mask)
    
@transformation
def rotate(image, angle):
    """Return a rotated image."""
    return scipy.ndimage.interpolation.rotate(image, angle)

@transformation
def apply_mask(image, mask):
    """Return a masked image."""
    return image * mask

@transformation
def remove_large_regions(segmentation, max_size=5000):
    """Return a masked image."""
    for i in segmentation.identifiers:
        region = segmentation.region_by_identifier(i)
        if region.area > max_size:
            segmentation[np.where(region)] = 0
    return segmentation
