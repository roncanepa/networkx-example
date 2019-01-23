import argparse
import pickle
import random

def main():
    args = parse_args()

    with open("./computed-data/all-providers.pickle", "r") as infile:
        all_providers = pickle.load(infile)

    random.seed(args.seed)

    subset = random.sample(all_providers, args.providers)

    with open("./computed-data/subset-providers.pickle", "w") as outfile:
        pickle.dump(subset, outfile)

    for p in subset:
        print p

    print "length of subset is %i" % len(subset)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--providers', type=int, default=100, help='number of providers')
    parser.add_argument('--seed', type=int, default=1234567890, help='seed to pass to random')

    return parser.parse_args()

if __name__ == '__main__':
    main()
