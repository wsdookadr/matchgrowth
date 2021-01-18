About
=====

This module provides a CLI tool for rough approximations according to a catalog
of prescribed growth rates.

The tool currently features most well-known [classes of growth rates](https://en.wikipedia.org/wiki/Time_complexity#Table_of_common_time_complexities)
and works by fitting each generic growth rate function to the given data.

Its primary use case is [analyzing time or space growth rates](https://en.wikipedia.org/wiki/Analysis_of_algorithms#Growth_rate_analysis_of_other_resources) of various
algorithms, but it can also be used on data coming from physical measurements.

Install
=======

To install from pypi:

    pip3 install --user matchgrowth

Usage
=====

The CLI tool expects to be passed through `--infile` a CSV file, and through `--col1` and `--col2` two column names
present inside the CSV file. Currently the CSV file needs to have headers for all columns.

The `--top` parameter allows to limit the number of matched growth rates reported.

The `--outfile` parameter is optional and allows to write the generated plot to a PNG file on disk.
If the `--outfile` parameter is not passed, the default GUI from matplotlib will be used to display the plot.

    usage: match-growth.py [-h] --infile INFILE [--outfile OUTFILE] --col1 COL1
                           --col2 COL2 [--top TOP]

    Tool for estimating growth rates

    optional arguments:
      -h, --help         show this help message and exit
      --infile INFILE    CSV input file with measurements
      --outfile OUTFILE  PNG file to write the plot to
      --col1 COL1        data column 1 from the CSV
      --col2 COL2        data column 2 from the CSV
      --top TOP          only print top N closest growth rates

Example usage:

    match-growth.py --infile ./tests/modif7_bench.txt --outfile r1.png --col1 N --col2 memory --top 2

<img src="https://raw.githubusercontent.com/wsdookadr/matchgrowth/master/example.png" alt="drawing" style="width:200px;"/>

Support
==================

For questions or requests for paid support, please send an e-mail to business@garage-coding.com

