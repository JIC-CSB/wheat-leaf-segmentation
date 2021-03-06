"""Segment the tissue."""

import warnings

import numpy as np

import skimage.morphology

from align import find_angle

from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation
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
    dilation_binary,
    rotate,
    apply_mask,
    remove_large_regions,
    invert_binary,
)

# Suppress spurious scikit-image warnings.
warnings.filterwarnings("ignore", module="skimage.exposure._adapthist")
warnings.filterwarnings("ignore", module="skimage.util.dtype")
warnings.filterwarnings("ignore", module="skimage.io._io")


@transformation
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


def vertical_cuts(thresholded_image):
    """Return vertical cuts to separate fused seeds."""
    n = 50
    selem = np.array([0, 1, 0] * n).reshape((n, 3))
    cuts = invert_binary(thresholded_image)
    cuts = connected_components(cuts, background=0)
    cuts = remove_large_regions(cuts, max_size=500).astype(bool)
    cuts = dilation_binary(cuts, selem=selem)
    cuts = invert_binary(cuts)
    return cuts


@transformation
def remove_cells_touching_border(segmentation, image):
    """Remove cells that touch the border."""
    for i in segmentation.identifiers:
        region = segmentation.region_by_identifier(i)
        outline = region.dilate(2).border
        touching_pixels = image[np.where(outline)]
        if np.min(touching_pixels) == 0:
            segmentation[np.where(region)] = 0
    return segmentation


@transformation
def remove_squiggly_cells(segmentation):
    for i in segmentation.identifiers:
        region = segmentation.region_by_identifier(i)
        squiggle_factor = float(region.perimeter) / float(region.area)
        if squiggle_factor < 0.3:
            segmentation[np.where(region)] = 0
    return segmentation


@transformation
def remove_tilted_cells(segmentation):
    props = skimage.measure.regionprops(segmentation)
    for p in props:
        region = segmentation.region_by_identifier(p.label)
        if abs(p.orientation) < 1.309:  # 75 degrees in radians
            segmentation[np.where(region)] = 0
    return segmentation


def segment(image):
    """Return a segmented image and rotation angle."""
    angle = find_angle(image)
    image = rotate(image, angle)
    mask = create_mask(image)

    watershed_mask = equalize_adaptive_clahe(image)
    watershed_mask = smooth_gaussian(watershed_mask, sigma=(1, 0))
    watershed_mask = threshold_otsu(watershed_mask)
    watershed_mask = apply_mask(watershed_mask, mask)

    n = 20
    selem = np.array([0, 1, 0] * n).reshape((n, 3))
    seeds = erosion_binary(watershed_mask, selem=selem)
    seeds = apply_mask(seeds, vertical_cuts(watershed_mask))
    seeds = remove_small_objects(seeds)
    seeds = connected_components(seeds, connectivity=1, background=0)

    segmentation = watershed_with_seeds(image, seeds, mask=watershed_mask)
    segmentation = remove_cells_touching_border(segmentation, image)
    segmentation = remove_cells_touching_border(segmentation, mask)
    segmentation = remove_tilted_cells(segmentation)

    return segmentation, angle


def main():
    image = argparse_get_image()
    segment(image)

if __name__ == "__main__":
    main()
