"""Annotate the segmented tissue."""

import skimage.draw

from jicbioimage.core.transform import transformation
from jicbioimage.illustrate import AnnotatedImage
from jicbioimage.core.util.array import _pretty_color

from util import argparse_get_image
from segment import segment
from transform import rotate


def annotate_segmentation(image, segmentation):
    """Return annotated segmentation."""
    annotation = AnnotatedImage.from_grayscale(image)
    for i in segmentation.identifiers:
        region = segmentation.region_by_identifier(i)
        color = _pretty_color()
        annotation.mask_region(region.border.dilate(), color)

    props = skimage.measure.regionprops(segmentation)

    for p in props:

        minr, minc, maxr, maxc = p.bbox
        cval = int(p.centroid[1])
        line = skimage.draw.line(minr, cval, maxr, cval)
        annotation.mask_region(line, (0, 255, 0))

    return annotation


@transformation
def annotate(image):
    """Return annotated image."""
    segmentation, angle = segment(image)

    image = rotate(image, angle)
    return annotate_segmentation(image, segmentation)


def main():
    image = argparse_get_image()
    a = annotate(image)
    with open("annotated.png", "wb") as fh:
        fh.write(a.png())


if __name__ == "__main__":
    main()
