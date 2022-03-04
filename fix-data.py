import sys, argparse, csv, os

#Perform an operation(s) on a row.
def fill_row(row, lastRow):
    if row['Practitioner'] == "":
        row['Practitioner'] = lastRow['Practitioner']
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
    parser.add_argument('-o', type=str, nargs='?', help="Name of the file for the output", required=False)

    # Parse and print the results
    args = parser.parse_args()
    if args.i == None:
        parser.print_help()
    else:
        if args.o == None:
            #if no default output name is set then use output.csv
            args.o = "output.csv"
        do_work(args.i, args.o)