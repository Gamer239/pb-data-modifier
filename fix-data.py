__author__ = "Gamer239"
__copyright__ = "Copyright (C) 2022 Gamer239"
__license__ = "General Public Licence v2"
__version__ = "1.0"

import sys, argparse, csv, os, copy, math

#Perform an operation(s) on a row.
def fill_row(row, lastRow):
    #Fill in the practitioner if needed.
    #This data should stay the same between line items since only 1 Practitioner can be assigned to a 
    #transaction even if it contains multiple line items.
    if row['Practitioner'] == "":
        row['Practitioner'] = lastRow['Practitioner']

    #Set the AmountPaid item if it has no value.
    #Set to 0 since any other value would mess up further calculations.
    #Other payment info in a transaction can pull data from LineItem* fields
    if row['AmountPaid'] == "":
        row['AmountPaid'] = 0.00
    return(row)

#Convert a string based number to a float by shifting precision before converting to a float
def string_to_float(number):
    if type(number) == str and number != 'X':
        leftside = float(number.split('.',1)[0])
        rightside = float(number.split('.',1)[1].split('%')[0])
        leftside = leftside * 100
        number = leftside + rightside
    elif type(number) == str and number == 'X':
        number = float(0.0)
    return(number)

def float_to_string(number):
    if type(number) == float:
        shiftnum = 100
        rightside = math.fmod(number, shiftnum)
        if number >= 0:
            leftside = number - rightside
        else:
            leftside = number + rightside
        leftside = leftside / shiftnum
        number = str(int(leftside)) + "." + str(int(rightside)).zfill(2)
    return(number)

#Add the current row data to the sum totals and return the updated values
def sum_row(row, sum_fields, current_sums):
    #Save a copy of the row to manipulate
    sums = copy.deepcopy(row)

    #Loop through each of the field names
    for field in sum_fields:

        #Check of the field name exists in the row
        if field in current_sums.keys():

            #Check if the field contents are only numeric
            if type(sums[field]) == float or (len(sums[field]) >= 1 and sums[field].replace('.','',1).isdigit()):
                if len(str(current_sums[field])) == 0:
                    current_sums[field] = 0.0
                sums[field] = string_to_float(sums[field]) + string_to_float(current_sums[field])
            #Carry over the data if the field is X (This can apply to LineItemProfit)
            elif sums[field] == 'X':
                sums[field] = current_sums[field]
            elif len(sums[field]) >= 1:
                sums[field] = sums[field] + current_sums[field]
                if len(sums[field]) > 1000:
                    print("Error: You're trying to perform a sum operation on a string. Check your -s arguments.")
                    exit()
            #Carry over the data if the new field is blank
            elif len(sums[field]) == 0:
                sums[field] = current_sums[field]

    #Convert floats back to proper values
    for field in sum_fields:
        sums[field] = float_to_string(sums[field])
            
    #return the new sum dictionary row
    return(sums)

#Return whether or not the row matches the given filters
def does_match_filter(row, filter_args):
    filter_match = True
    for filter in filter_args:
        #Sanity check that we are given the delimeter between column name and value(s)
        if filter.find("=") == -1:
            print("Error: Filters must contain the = character between the column and values")
            exit()
        
        #Grab the column name
        columnName = filter.split("=", 1)[0]

        #Grab the list of acceptable Values
        valueList = filter.split("=", 1)[1].split(",")

        #Sanity check to make sure that the column name exists in the data 
        if columnName not in row.keys():
            print("Error: Invalid Column Name not found in row. Check your filter argument or data")
            exit()

        #if one part of the filter doesn't match then return without processing any more of the data
        if row[columnName] not in valueList:
            filter_match = False
            break
    return(filter_match)

#Shorten a cell's information by searching for a substring and setting the cell's contents to the substring
def shorten_data(row, shorten_args):
    shortrow = copy.deepcopy(row)
    for shortstr in shorten_args:
        #Sanity check that we have a = sign declared before splitting to column and value
        if shortstr.find("=") == -1:
            print("Error: String to shorten must contain the = character between the column and values")
            exit()
        
        #Grab the column name
        columnName = shortstr.split("=", 1)[0]

        #Grab the list of acceptable strings
        valueList = shortstr.split("=", 1)[1].split(",")

        #Sanity check to make sure that the column name exists in the data 
        if columnName not in row.keys():
            print("Error: Invalid Column Name not found in row. Check your shorten argument or data")
            exit()

        #Search for the existance of any of the values
        #in the column data
        for value in valueList:
            if row[columnName].find(value) >= 0:
                shortrow[columnName] = value
                break

    return(shortrow)

#Read and return the supplemental csv
def read_supplemental_csv(filename):
    #Check to make sure that the input file exists and exit on error
    if os.path.isfile(filename) == False:
        print("Error: Supplemental input file not found")
        exit()

    csvcontents = csv.DictReader(open(filename, newline='', encoding='utf8'))
    return(csvcontents)

#Take in the filter argument strings one at a time and turn them into valid string filters
def build_filters(filter_args):
    filters = []
    built_row = {}
    for item in filter_args:
        filename = item.split("|", 1)[0]
        file_filters = read_supplemental_csv(filename)
        spacer = item.split("|", 2)[1]
        fields = item.split("|", 2)[2]

        #Create each filter from each row of the data
        for row in file_filters:
            filter = ""
            built_row = {}
            for field in fields.split("|"):
                #Add the spacer only if we already have a something in the filter string
                if len(filter) > 0:
                    filter = filter + spacer

                #Add either the found variable or the text itself to the filter string
                if field in row:
                    filter = filter + row[field]
                else:
                    filter = filter + field
            
            built_row = row
            built_row["filter"] = filter
            filters.append(built_row)
            
    return filters

def compute_lineitemprofit(row, filters, profit_math):
    found = False
    for filter in filters:
        #Make sure the filter value exists
        if "filter" not in filter:
            continue
        
        #Make sure the Line Item Description exists
        if "LineItemDescription" not in row:
            continue

        #Make sure that we have something to compute against
        if "LineItemSubTotal" not in row:
            continue

        if type(profit_math["cog"]) != str or len(profit_math["cog"]) <= 0:
            print("Cost of Goods String Error")
            exit()

        if profit_math["cog"] not in filter:
            print("Column '" + profit_math["cog"] + "' is not found in filter")
            exit()

        if type(profit_math["fee"]) != str or len(profit_math["fee"]) <= 0:
            print("Fee String Error")
            exit()

        if profit_math["fee"] not in filter:
            print("Column '" + profit_math["fee"] + "' is not found in filter")
            exit()

        #Determine if the filter is in the description
        if filter["filter"] in row["LineItemDescription"]:
            subtotal = string_to_float(row["LineItemSubTotal"])
            cog = string_to_float(filter[profit_math["cog"]])
            fee = string_to_float(filter[profit_math["fee"]])
            profit = ( ( subtotal * ( 100 - fee ) ) / 100 ) - cog
            row["LineItemProfit"] = float_to_string( profit )
            found = True

    if found == False:
        row["LineItemProfit"] = 'X'

    return row

def do_work(args):
    #convert args to variables
    filename = args.i
    outputfilename = args.o
    sum_args = args.s
    filter_args = args.f
    shorten_args = args.shorten
    output_header_only = args.column_names
    profit_args = [ args.p ]
    profit_math = { "cog" : args.cog, "fee" : args.fee_percent }
    
    #Check to make sure that the input file exists and exit on error
    if os.path.isfile(filename) == False:
        print("Error: Input file not found")
        exit()

    #Open the input file for reading
    with open(filename , newline='', encoding='utf8') as csvfile:
        csvcontents = csv.DictReader(csvfile)

        #Initialize lastrow contents
        lastRow = ""

        #Initialize sum contents
        sum_data = {}

        #Fetch Filters For Profit Calculations
        if args.p != None:
            profit_filter = build_filters(profit_args)
            csvcontents.fieldnames.append("LineItemProfit")

        #Output the column names and quit if asked
        if output_header_only == True:
            print("Valid Column Names:\n")
            print(*csvcontents.fieldnames, sep='\n')
            exit()

        #open the output file for writing the modified results
        with open(outputfilename, 'w', newline='', encoding='utf8') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=csvcontents.fieldnames)

            #Write the CSV Header Information
            writer.writeheader()

            #Iterate through each data row in the table
            for row in csvcontents:
                #save the current row with any data modified from fill_row
                row = fill_row(row, lastRow)

                #Shorten data only if shorten arguments were specified
                if shorten_args != None:
                    row = shorten_data(row, shorten_args)

                #Compute profit
                if args.p != None:
                    row = compute_lineitemprofit(row, profit_filter, profit_math)

                #save the current row to use for the next row's calculations
                lastRow = row

                #Test if the data matches the filter
                #Ignore the sum and writing if the data doesn't match the filter
                if filter_args != None and does_match_filter(row, filter_args) == False:
                    continue

                #Add the sum data if it was defined in the arguments
                if sum_args != None:
                    sum_data = sum_row(row, sum_args, sum_data)

                #write the modified row to the output file
                writer.writerow(row)

        #Check to see if the sum argument was added
        if sum_args != None:
            #Loop through each sum argument
            for field in sum_args:
                #Check of the provided argument has a key in the computed dictionary
                if field in sum_data.keys():
                    #print the computed result
                    print("For field: " + field + " the total is " + str(float_to_string(sum_data[field])))

if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, nargs='?', help="Name of the input file", required=True)
    parser.add_argument('-o', type=str, nargs='?', help="Name of the file for the output (Default=output.csv)", required=False, default="output.csv")
    parser.add_argument('-s', nargs='+', help="A space separated list of fields names to sum", required=False)
    parser.add_argument('-f', nargs='+', help="Only output or compute a result when column=value or column=value,value2,etc. Note: Do NOT put commas in the filter values.", required=False)
    parser.add_argument('-shorten', nargs='+', help="Shorten the text of data to the text specified in the specified column. column=ShortenedValue. Note: Do NOT include commas in the strings to shorten. Shortening happens before filtering.", required=False)
    parser.add_argument('--column-names', action='store_true', help="List the names of the columns in the imported CSV and exit", required=False)
    parser.add_argument('-p', nargs='?', help="Use an additional file to calculate a line item profit", required=False, const="Supplements.csv| |*|Supplement Company|Supplement Name")
    parser.add_argument('-cog', type=str, nargs='?', help="Cost of Goods - Used for computing the line item profit only. The name of the column should be set here.", required=False, default="Supplement's Cost to the Business")
    parser.add_argument('-fee-percent', type=str, nargs='?', help="Fee Percent - Used for computing the line item profit only. The name of the column should be set here.", required=False, default="Supplement Fee Percent")

    # Parse and print the results
    args = parser.parse_args()
    if args.i == None:
        parser.print_help()
    else:
        do_work(args)