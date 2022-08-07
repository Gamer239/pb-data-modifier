# Practice Better Exported Data Modification Tools
This repo exists to make easy modifications to data that is exported from Practice Better. Currently Practice Better outputs most of the relevant information on a single line. If you have multiple items in an invoice this information does not extend to these extra lines. This set of scripts will help Excel work with the data easier by filling in the missing data.

## Requirements
Python 3

Install the requirements:

`pip install -r requirements.txt`

or

`pip3 install -r requirements.txt`

if python3 is not your default interpreter.

## Usage
usage: fix-data.py [-h] -i [I] [-o [O]] [-s S [S ...]] [-f F [F ...]] [-shorten SHORTEN [SHORTEN ...]] [--column-names]

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

  --column-names        List the names of the columns in the imported CSV and exit

  -p P [P ...]          Use an additional file to calculate a line item profit

  -cog [COG]            Cost of Goods - Used for computing the line item profit only. The name  of the column should be set here.

  -fee-percent [FEE_PERCENT]
                        Fee Percent - Used for computing the line item profit only. The name of the column should be set
                        here.

  -partial-supplement-string [PARTIAL_SUPPLEMENT_STRING]
                        Define the string that will be used to determine if the X warning is needed

  -supress-x            Supress a warning about X being found

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

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe,Jane Doe"`

Look for a specific set of data where multiple filters apply.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe" "LineItemAmount=3.50"`

Look for a specific set of data where multiple filters and multiple data values apply.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe,Jane Doe" "LineItemAmount=3.50,8.50"`

### Shorten Examples

Shorten a cell's contents

`python fix-data.py -i Invoices-19800101-19800131.csv -shorten "LineItemDescription=New Client"`

Shorten multiple cells in the same column

`python fix-data.py -i Invoices-19800101-19800131.csv -shorten "LineItemDescription=New Client,Phone Client"`

Shorten multiple columns

`python fix-data.py -i Invoices-19800101-19800131.csv -shorten "Practitioner=Joe" "LineItemDescription=New Client"`

### Column Name Example
Output the names of the columns. This is useful for getting information for the filter argument without doing any data processing.

`python fix-data.py -i Invoices-19800101-19800131.csv --column-names`

### Supplemental Profit Examples
Compute the profit based on a supplemental file. The profit will be added on as a LineItemProfit line whenever the flag is used. The separator | **must** be used between each item (if specified).

Compute the profit with the default column names

`python3 fix-data.py -i input.csv -p`

Compute the profit by specifing the LineItemDesciption search parameters. Before the first | denotes the file name. The next section denotes the spacing and the remaining denote the search strings.

To illustrate further <filename>|<spacer>|search params. If one of the search params matches a column name in the supplemental file then the corresponding column's value will be used. If the column name doesn't match then the text will be used instead.

`python3 fix-data.py -i input.csv -p "Supplements.csv| |*|Supplement Company|Supplement Name"`

For the example above, * does not match any column name so its value is used directly. Supplement Company and Supplement Name match column header names in a CSV and therefore the value of the row is used instead.

#### Cost of Good Column Name

The cost of good column name can be customized when calculating the profit.

#### Fee Percent Column Name

The fee percent column name can be customized when calculating the profit.

### Combination Examples
Filter data based on the Practitioner John Doe and output the AmountPaid for any column that John Doe is in.

`python fix-data.py -i Invoices-19800101-19800131.csv -s AmountPaid -f "Practitioner=John Doe"`

Find the sum of the AmountPaid to practitioner John Doe but only when John Doe's LineItemAmount was 3.50

`python fix-data.py -i Invoices-19800101-19800131.csv -s AmountPaid -f "Practitioner=John Doe" "LineItemAmount=3.50"`

Filter and shorten data based on Practitioner Joe and his "New Client" rows. Note: Shorting happens BEFORE filtering.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe" -shorten "LineItemDescription=New Client"`

Filter, shorten, and sum data. Note: Shortening happens BEFORE filtering.

`python fix-data.py -i Invoices-19800101-19800131.csv -f "Practitioner=John Doe" "LineItemAmount=3.50" -shorten "LineItemDescription=New Client,Phone Client" -s Total AmountPaid`
