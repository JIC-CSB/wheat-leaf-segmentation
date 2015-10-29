"""Create histogram of lengths of cells in tissue."""

import skimage.measure
import matplotlib.pyplot as plt

from util import argparse_get_image
from segment import segment


def length_histogram(image):
    """Create histogram of cell lengths."""
    segmentation, angle = segment(image)
    props = skimage.measure.regionprops(segmentation)
    lengths = [p["major_axis_length"] for p in props]
    plt.hist(lengths)
    plt.xlabel("Major axis cell length (pixels)", fontsize=16)
    plt.ylabel("Frequency", fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.savefig("length_histogram.png")


def main():
    image = argparse_get_image()
    length_histogram(image)


if __name__ == "__main__":
    main()
