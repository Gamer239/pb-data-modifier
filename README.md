# Practice Better Exported Data Modification Tools
This repo exists to make easy modifications to data that is exported from Practice Better. Currently Practice Better outputs most of the relevant information on a single line. If you have multiple items in an invoice this information does not extend to these extra lines. This set of scripts will help Excel work with the data easier by filling in the missing data.

## Requirements
Python 3

## Usage
usage: fix-data.py [-h] -i [I] [-o [O]] [-s S [S ...]] [-f F [F ...]] [-shorten SHORTEN [SHORTEN ...]]

optional arguments:
  -h, --help            show this help message and exit

  -i [I]                Name of the input file

  -o [O]                Name of the file for the output (Default=output.csv)

  -s S [S ...]          A space separated list of fields names to sum

  -f F [F ...]          Only output or compute a result when column=value or column=value,value2,etc. Note: Do NOT put
                        commas in the filter values.

  -shorten SHORTEN [SHORTEN ...]
                        Shorten the text of data to the text specified in the specified column. column=ShortenedValue.
                        Note: Do NOT include commas in the strings to shorten. Shortening happens before filtering.

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

### Shorten Examples

Shorten a cell's contents

`python fix-data.py -i Invoices-19800101-19800131.csv -shorten "LineItemDescription=New Client"`

Shorten multiple cells in the same column

`python fix-data.py -i Invoices-19800101-19800131.csv -shorten "LineItemDescription=New Client,Phone Client"`

Shorten multiple columns

`python fix-data.py -i Invoices-19800101-19800131.csv -shorten "Practitioner=Joe" "LineItemDescription=New Client"`

### Combination Examples
Filter data based on the Practitioner John Doe and output the AmountPaid for any column that John Doe is in.

`python fix-data.py -i Invoices-19800101-19800131.csv -s AmountPaid -f "Practitioner=John Doe"`

Find the sum of the AmountPaid to practitioner John Doe but only when John Doe's LineItemAmount was 3.50

`python fix-data.py -i Invoices-19800101-19800131.csv -s AmountPaid -f "Practitioner=John Doe" "LineItemAmount=3.50"`

Filter and shorten data based on Practitioner Joe and his "New Client" rows. Note: Shorting happens BEFORE filtering.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe" -shorten "LineItemDescription=New Client"`

Filter, shorten, and sum data. Note: Shortening happens BEFORE filtering.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe" "LineItemAmount=3.50" -shorten "LineItemDescription=New Client,Phone Client" -s Total AmountPaid`
