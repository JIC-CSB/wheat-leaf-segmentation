# README

Create an annotated segmentation for a series in the microscopy image.
The command below produces the file ``annotated.png`` containing an
annotated image of the segmentation of the first series (indexed as 0).

```
python scripts/annotate.py data/raw/As+1_top.lif 0
```

Plot a histogram of the cell lengths for a series in the microscopy image.
The command below produces the file ``length_histogram.png`` containing an
histogram of the lengths of the segmented cells in the first series.

```
python scripts/length_histogram.py data/raw/As+1_top.lif 0
```
