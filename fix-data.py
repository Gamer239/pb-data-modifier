import sys, argparse, csv, os, copy

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
                sums[field] = float(sums[field]) + float(current_sums[field])
            elif len(sums[field]) >= 1:
                sums[field] = sums[field] + current_sums[field]
                if len(sums[field]) > 1000:
                    print("Error: You're trying to perform a sum operation on a string. Check your -s arguments.")
                    exit()
            #Carry over the data if the new field is blank
            elif len(sums[field]) == 0:
                sums[field] = current_sums[field]
            
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

def do_work(filename, outputfilename, sum_args, filter_args, shorten_args):
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
                    print("For field: " + field + " the total is " + str(sum_data[field]))

if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, nargs='?', help="Name of the input file", required=True)
    parser.add_argument('-o', type=str, nargs='?', help="Name of the file for the output (Default=output.csv)", required=False, default="output.csv")
    parser.add_argument('-s', nargs='+', help="A space separated list of fields names to sum", required=False)
    parser.add_argument('-f', nargs='+', help="Only output or compute a result when column=value or column=value,value2,etc", required=False)
    parser.add_argument('-shorten', nargs='+', help="Shorten the text of data to the text specified in the specified column. column=ShortenedValue", required=False)

    # Parse and print the results
    args = parser.parse_args()
    if args.i == None:
        parser.print_help()
    else:
        do_work(args.i, args.o, args.s, args.f, args.shorten)