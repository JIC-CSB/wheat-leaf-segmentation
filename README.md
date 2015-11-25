# README

## Windows installation

Install the [Anaconda Python distribution](http://continuum.io/downloads).

Setup a virtual environment named ``venv`` and install the scientific Python
package dependencies.

```
conda create –n venv python=2.7 numpy scipy scikit-image
```

Activate the virtual environment.

```
activate venv
```

Install the ``jicbioimage`` dependencies.

```
pip install jicbioimage.core
pip install jicbioimage.transform
pip install jicbioimage.segment
pip install jicbioimage.illustrate
```

Follow the
[jicbioimage installation notes](http://jicbioimage.readthedocs.org/en/latest/installation_notes.html)
to install ``freeimage`` and ``bioformats``.

Download the
[wheat segementation](https://githq.nbi.ac.uk/jic-image-analysis/wheat-segmentation)
project from githq and go into it.


## Data analysis

On Windows remember to activate the virtual environment when you open a new
command prompt.

```
activate venv
```

Run the analysis.

```
python scripts/wheat_variety_analysis.py /path/to/raw/file/of/interest.lif output_directory
```

This will produce a file named ``cell_lengths.csv`` in the output directory
along with a number of annotated images. Look at the images and decide if
any series need to be excluded from the ``cell_lengths.csv`` file due to poor
segmentation results.

Use your curated ``cell_lengths.csv`` file as input for your statistical analysis.
