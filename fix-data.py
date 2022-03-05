import sys, argparse, csv, os

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
    sums = row

    #Loop through each of the field names
    for field in sum_fields:

        #Check of the field name exists in the row
        if field in current_sums.keys():

            #Check if the field contents are only numeric
            if type(sums[field]) == float or sums[field].replace('.','',1).isdigit():
                sums[field] = float(sums[field]) + float(current_sums[field])
            else:
                sums[field] = sums[field] + current_sums[field]
                if len(sums[field]) > 1000:
                    print("Error: You're trying to perform a sum operation on a string. Check your -s arguments.")
                    exit()
            
    #return the new sum dictionary row
    return(sums)


def do_work(filename, outputfilename, sum_args):
    #Check to make sure that the input file exists and exit on error
    if os.path.isfile(filename) == False:
        print("Error: Input file not found")
        exit()

    #Open the input file for reading
    with open(filename , newline='', encoding='utf8') as csvfile:
        csvcontents = csv.DictReader(csvfile)

        #Initialize lastrow contents
        lastRow = ""

        #nitialize sum contents
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

                #save the current row to use for the next row's calculations
                lastRow = row

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

    # Parse and print the results
    args = parser.parse_args()
    if args.i == None:
        parser.print_help()
    else:
        do_work(args.i, args.o, args.s)