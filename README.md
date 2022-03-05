# Practice Better Exported Data Modification Tools
This repo exists to make easy modifications to data that is exported from Practice Better. Currently Practice Better outputs most of the relevant information on a single line. If you have multiple items in an invoice this information does not extend to these extra lines. This set of scripts will help Excel work with the data easier by filling in the missing data.

## Requirements
Python 3

## Usage
usage: fix-data.py [-h] -i [I] [-o [O]] [-s S [S ...]] [-f F [F ...]]

optional arguments:

  -h, --help    show this help message and exit

  -i [I]        Name of the input file

  -o [O]        Name of the file for the output (Default=output.csv)

  -s S [S ...]  A space separated list of fields names to sum

  -f F [F ...]  Only output or compute a result when column=value

## Examples
### Simple Examples
Providing a simple input file.

`python fix-data.py -i input.csv`

Providing a simple input file and declaring a custom filename.

`python fix-data.py -i Invoices-19800101-19800131.csv -o custom-out-filename.csv`

### Sum Examples
Compute the sum of a column.

`python fix-data.py -i Invoices-19800101-19800131.csv -s AmountPaid`

### Filter Examples
Filter the data based on a Practitioner.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe"`

Filter the data such that you are looking for data from John and Jane Doe

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe, Jane Doe"`

Look for a specific piece of data where multiple filters apply.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe" "LineItemAmount=3.50"`

### Combination Examples
Filter data based on the Practitioner John Doe and output the AmountPaid for any column that John Doe is in.

`python fix-data.py -i Invoices-19800101-19800131.csv -s AmountPaid -f "Practitioner=John Doe"`

Find the sum of the AmountPaid to practitioner John Doe but only when John Doe's LineItemAmount was 3.50

`python fix-data.py -i Invoices-19800101-19800131.csv -s AmountPaid -f "Practitioner=John Doe" "LineItemAmount=3.50"`
