import sys, argparse, csv, os

def fill_row(row, lastRow):
    if row['Practitioner'] == "":
        row['Practitioner'] = lastRow['Practitioner']
    if row['AmountPaid'] == "":
        row['AmountPaid'] = 0.00
    return(row)

def do_work(filename, outputfilename):
    if os.path.isfile(filename) == False:
        print("Error: Input file not found")
        exit()

    #Open the input file for reading
    with open(filename , newline='', encoding='utf8') as csvfile:
        csvcontents = csv.DictReader(csvfile)
        lastRow = ""

        #open the output file
        with open(outputfilename, 'w', newline='', encoding='utf8') as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=csvcontents.fieldnames)
            writer.writeheader()
            for row in csvcontents:
                #fill in the row's contents
                row = fill_row(row, lastRow)

                #save the last row
                lastRow = row

                #write the modified row to the output file
                writer.writerow(row)

if __name__ == '__main__':
    # Create the parser and add arguments
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