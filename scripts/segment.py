"""Segment the tissue."""

import numpy as np

import skimage.morphology

from align import find_angle

from jicbioimage.core.image import Image
from jicbioimage.segment import connected_components, watershed_with_seeds
from jicbioimage.transform import (
    equalize_adaptive_clahe,
    smooth_gaussian,
    threshold_otsu,
    remove_small_objects,
)

from util import argparse_get_image
from transform import (
    erosion_binary,
    rotate,
    apply_mask,
    remove_large_regions,
)

def create_mask(image):
    """Return a mask for the region of interest."""
    selem = skimage.morphology.disk(2)
    im = equalize_adaptive_clahe(image)
    im = threshold_otsu(im)
    im = erosion_binary(im, selem)
    mask = np.ones(im.shape, dtype=bool)
    segmentation = connected_components(im, background=0)
    for i in segmentation.identifiers:
        region = segmentation.region_by_identifier(i)
        if region.area > 5000:
            mask[np.where(region.convex_hull)] = False
    return Image.from_array(mask)

def segment(image):
    """Return a segmented image and rotation angle."""
    angle = find_angle(image)
    image = rotate(image, angle)

    im = equalize_adaptive_clahe(image)
    im = smooth_gaussian(im, sigma=(1, 0))
    im = threshold_otsu(im)
    watershed_mask = im

    n = 20
    selem = np.array([0,1,0]*n).reshape((n,3))
    im = erosion_binary(im, selem=selem)

    mask = create_mask(image)

    im = apply_mask(im, mask)
    im = remove_small_objects(im)

    segmentation = connected_components(im, connectivity=1, background=0)

    watershed_mask = apply_mask(watershed_mask, mask)
    segmentation = watershed_with_seeds(image, segmentation, mask=watershed_mask)

    return segmentation, angle


def main():
    image = argparse_get_image()

    segment(image)
    


if __name__ == "__main__":
    main()
