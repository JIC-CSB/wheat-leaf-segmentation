"""Annotate the segmented tissue."""

from jicbioimage.core.transform import transformation
from jicbioimage.illustrate import AnnotatedImage
from jicbioimage.core.util.array import _pretty_color

from align import find_angle
from util import argparse_get_image
from segment import segment
from transform import rotate

@transformation
def annotate(image):
    """Return annotated image."""
    segmentation, angle = segment(image)

    image = rotate(image, angle)
    annotation = AnnotatedImage.from_grayscale(image)
    for i in segmentation.identifiers:
        region = segmentation.region_by_identifier(i)
        color = _pretty_color()
        annotation.mask_region(region.border, color)
    return annotation

def main():
    image = argparse_get_image()
    annotate(image)
    


if __name__ == "__main__":
    main()
