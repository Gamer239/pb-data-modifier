# Practice Better Exported Data Modification Tools
This repo exists to make easy modifications to data that is exported from Practice Better. Currently Practice Better outputs most of the relevant information on a single line. If you have multiple items in an invoice this information does not extend to these extra lines. This set of scripts will help Excel work with the data easier by filling in the missing data.

## Requirements
Python 3

## Usage
usage: fix-data.py [-h] -i [I] [-o [O]]

optional arguments:
  -h, --help  show this help message and exit
  -i [I]      Name of the input file
  -o [O]      Name of the file for the output (Default=output.csv)

## Examples
Providing a simple input file

`python fix-data.py -i input.csv`

Providing a simple input file and declaring a custom filename

`python fix-data.py -i Invoices-19800101-19800131.csv -o custom-out-filename.csv`
