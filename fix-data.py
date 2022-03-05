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

def do_work(filename, outputfilename):
    #Check to make sure that the input file exists and exit on error
    if os.path.isfile(filename) == False:
        print("Error: Input file not found")
        exit()

    #Open the input file for reading
    with open(filename , newline='', encoding='utf8') as csvfile:
        csvcontents = csv.DictReader(csvfile)

        #Initialize lastrow contents
        lastRow = ""

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

                #write the modified row to the output file
                writer.writerow(row)

if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, nargs='?', help="Name of the input file", required=True)
    parser.add_argument('-o', type=str, nargs='?', help="Name of the file for the output (Default=output.csv)", required=False, default="output.csv")

    # Parse and print the results
    args = parser.parse_args()
    if args.i == None:
        parser.print_help()
    else:
        do_work(args.i, args.o)