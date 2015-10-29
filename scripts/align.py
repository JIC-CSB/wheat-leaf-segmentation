"""Align the tissue."""

import argparse

import skimage.morphology
import skimage.measure

from jicbioimage.core.transform import transformation
from jicbioimage.segment import connected_components
from jicbioimage.transform import (
    equalize_adaptive_clahe,
    threshold_otsu,
    remove_small_objects,
)

from util import get_microscopy_collection
from transform import rotate, erosion_binary


def find_angle(image):
    image = equalize_adaptive_clahe(image)
    image = threshold_otsu(image)
    image = erosion_binary(image, selem=skimage.morphology.disk(3))
    image = remove_small_objects(image, min_size=5000)
    segmentation = connected_components(image, background=0)
    properties = skimage.measure.regionprops(segmentation)
    angles = [p["orientation"] for p in properties]
    return sum(angles) / len(angles)

@transformation
def align(image):
    """Return an aligned image."""
    angle = find_angle(image)
    image = rotate(image, angle)
    return image

def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("input_file", help="path to raw microscopy data")
    parser.add_argument("series", type=int, help="microscopy series")

    args = parser.parse_args()
    microscopy_collection = get_microscopy_collection(args.input_file)

    image = microscopy_collection.image(s=args.series)
    image = image[:,:,0]

    align(image)
    


if __name__ == "__main__":
    main()
