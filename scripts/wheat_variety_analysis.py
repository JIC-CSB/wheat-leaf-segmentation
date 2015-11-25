"""Produce csv output from all series in a microscopy file."""

import os
import os.path
import argparse
import warnings

from jicbioimage.core.io import AutoWrite

from util import get_microscopy_collection
from segment import segment
from length_histogram import get_lengths
from transform import rotate
from annotate import annotate_segmentation


AutoWrite.on = False


def get_image(microscopy_collection, series):
    """Return microscopy image."""
    image = microscopy_collection.image(s=series)
    image = image[:, :, 0]
    return image

def write_csv_header(file_handle):
    """Write csv header to file handle."""
    file_handle.write("series,length")

def write_csv_row(series, length, file_handle):
    """Write csv row to file handle."""
    file_handle.write("{},{:.3f}\n".format(series, length))

def wheat_variety_analysis(microscopy_collection, output_dir):
    
    csv_fpath = os.path.join(output_dir, "cell_lengths.csv")
    with open(csv_fpath, "w") as csv_fh:
        write_csv_header(csv_fh)

        for s in microscopy_collection.series:
            print("Analysing series {}".format(s))

            # Write the CSV file.
            image = get_image(microscopy_collection, s)
            segmentation, angle = segment(image)

            for l in get_lengths(segmentation):
                write_csv_row(s, l, csv_fh)
            
            # Create annotated image.
            image = rotate(image, angle)        
            annotation = annotate_segmentation(image, segmentation)

            im_fpath = os.path.join(output_dir, "series_{:03d}.png".format(s))
            with open(im_fpath, "wb") as im_fh:
                im_fh.write(annotation.png())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("input_file", help="path to raw microscopy data")
    parser.add_argument("output_dir", help="output directory")

    args = parser.parse_args()
    microscopy_collection = get_microscopy_collection(args.input_file)

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    wheat_variety_analysis(microscopy_collection, args.output_dir)
