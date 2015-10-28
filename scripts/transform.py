"""Module containing image transformations."""

import scipy.ndimage.interpolation

from jicbioimage.core.transform import transformation

from jicbioimage.core.util.array import dtype_contract
import skimage.morphology

@transformation
@dtype_contract(input_dtype=bool, output_dtype=bool)
def erosion_binary(image, selem=None):
    return skimage.morphology.binary_erosion(image, selem)

@transformation
@dtype_contract(input_dtype=bool, output_dtype=bool)
def dilation_binary(image, selem=None):
    return skimage.morphology.binary_dilation(image, selem)

@transformation
def rotate(image, angle):
    """Return a rotated image."""
    return scipy.ndimage.interpolation.rotate(image, angle)
    

