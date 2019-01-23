import argparse
import logging
import pickle
from datetime import datetime, date
from patient_record import *


def patient_has_records_within_window(patients):
    last_datetime = datetime.min
    run_count = 1
    found_at_risk = False

    patients.sort(key=lambda x: x.FillDate)
    for r in patients:
        if found_at_risk:
            break
        # logging.info("next patient record date is %s and last_datetime is %s" % (r.FillDate, last_datetime))
        if r.FillDate > last_datetime:
            if run_count == 1:
                run_count += 1
                last_datetime = r.FillDate
                continue

            date_diff = r.FillDate - last_datetime
            logging.info(
                "run count: %i, \n\tlast_datetime is %s \n\tfilldate is %s" % (run_count, last_datetime, r.FillDate))
            logging.info("date diff is %f" % (date_diff).days)

            if date_diff.days < 30:
                found_at_risk = True

            last_datetime = r.FillDate
            run_count += 1
    logging.info("finished processing this patient, exiting function.")
    return found_at_risk


def main():
    args = parse_args()
    logging.basicConfig(filename=args.log, level=logging.INFO)

    logging.info("begin script.")

    # all records for single patient, used to examine date window
    current_patient_records = []

    # if deemed at-risk, stored here.
    at_risk_patients = set()

    all_providers = set()

    # a final dataset of parsed PatientRecords used for further processing
    structured_dataset = []

    # generated by build-drug-code-set.py
    drug_codes_of_interest = set()

    today = datetime.today()

    last_patient_id = ""

    with open("./computed-data/drug-code-sets-major-opioids.pickle", "r") as infile:
        drug_codes_of_interest = pickle.load(infile)

    logging.info("opening data file...")
    with open(args.input, 'rU') as infile:
        # skip header
        infile.readline()

        current_loop = 1
        for line in infile:
            line = line.strip()
            line_array = line.split(",")
            # logging.info("line date %s" % line_array[2])

            if current_loop == args.max_records:
                logging.info("hit max loop limit, breaking")
                break

            try:
                line_array[4] = datetime.strptime(line_array[2], "%m/%d/%Y")
            except ValueError:
                logging.error("could not parse date from patient FillDate data. tossing out this record. line array is: %s" % line_array )
                continue
            except:
                logging.error("unhandled exception in datetime parse.  line array is: %s" % line_array)
                raise

            r = PatientRecord(line_array)

            # we only care if it's a drug we're examining
            if r.ndc in drug_codes_of_interest:
                logging.info("drug code of interest, adding to structured_dataset...")
                structured_dataset.append(r)
            else:
                #logging.info("NOT drug code of interst. skipping and moving to next record.")
                current_loop += 1
                continue

            if r.PatientId != last_patient_id:

                # This means we need to stop and process all previous patient data first.
                logging.info("processing current patient %s " % last_patient_id)
                at_risk = patient_has_records_within_window(current_patient_records)
                logging.info("Finished processing patient.  at-risk is: %s" % at_risk)

                if at_risk:
                    at_risk_patients.add(last_patient_id)

                all_providers.add(r.PrescriberId)

                # now reset and handle the new one
                logging.info("now loading new patient: %s " % r.PatientId)
                current_patient_records = []
                last_patient_id = r.PatientId
                current_patient_records.append(r)
            else:
                #logging.info("appending entry for patientID %s to list" % r.PatientId)
                logging.info("appending entry for patientID %s to list: %s" % (r.PatientId, r))
                current_patient_records.append(r)

            current_loop += 1
            if current_loop % 10000 == 0:
                print "current loop is %i " % current_loop

    logging.info("done processing. we have %i at_risk patients. " % len(at_risk_patients))

    logging.info("pickling at risk patient set...")
    with open("./computed-data/at-risk-patients.pickle", "w") as output:
        pickle.dump(at_risk_patients, output)

    logging.info("pickling all providers...")
    with open("./computed-data/all-providers.pickle", "w") as output:
        pickle.dump(all_providers, output)

    logging.info("pickling structured dataset...")
    with open("./computed-data/structured-dataset.pickle", "w") as output:
        pickle.dump(structured_dataset, output)

    logging.info("end of script")



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--log', default='/dev/stderr', help='log file (default=stderr')
    parser.add_argument('--input', default='./original-data/minimal-dataset.csv', help='5-column raw input file')
    parser.add_argument('--out', default='/dev/stdout', help='output. default=stdout')
    parser.add_argument('--max_records', type=int, default=99999999999, help='maximum rows to process')

    return parser.parse_args()


if __name__ == '__main__':
    main()