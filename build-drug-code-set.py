import argparse
import logging
import pickle
import csv



def main():
    args = parse_args()

    logging.basicConfig(filename=args.log, level=logging.INFO)
    logging.info("begin script")

    drug_names = args.drug_names.split(",")
    drug_codes_of_interest = set()

    logging.info("gathering all codes for drug names %s " % drug_names)

    with open("./original-data/drug_table_jun2015b.csv", "r") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            # due to input data, all opoiids are at the top of the list, so we can stop processing.
            if row['drugcat'] != "1":
                logging.info("hit a non-opioid drugcat, halting reading.")
                break

            logging.info("line from data is %s " % row)

            for name in drug_names:
                logging.info("  checking for match on %s " % name)
                index = row['drug'].find(name)
                if index > -1:
                    logging.info("  found match on %s and adding to set.")
                    drug_codes_of_interest.add(row['ndcnum'])

    logging.info("done processing file.  pickling results...")

    with open("./computed-data/drug-code-sets-major-opioids.pickle", "w") as outfile:
        pickle.dump(drug_codes_of_interest, outfile)

    logging.info("length of drug_codes_of_interest is %i" % len(drug_codes_of_interest))

    logging.info("end of script")



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--log', default='/dev/stderr', help='log file (default=stderr')
    parser.add_argument('--out', default='/dev/stdout', help='output. default=stdout')
    parser.add_argument('--drug_names', default="Codeine,Dihydrocodeine,Hydrocodone,Methadone,Morphine,Oxycodone",
                        help='comma-delimited list of names for matching and included')

    return parser.parse_args()


if __name__ == '__main__':
    main()
