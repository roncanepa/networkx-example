

# Steps

Put `CY2014.csv` and drug_table_jun2015b.csv (or symlinks) into `./original-data`.

Do the following once:

```
cat ./original-data/sample-raw-data.csv  | cut -d, -f 1,8,10,12,13 > ./original-data/minimal-dataset.csv
```

Parse file and grab drug codes of interest into a `pickle` object:

```
python build-drug-code-set.py
```

create list of at-risk patients, grab a collection of all provider ids to be used later for subsetting, and bundle our data of interest into a pickle of PatientRecord objects

pass a --max_records arg to limit or for testing

```
python process-data.py --max_records=100000
```

select a random subset of providers:

```
python subset-providers.py --providers=1000
```

build the network:

```
python build-network.py
```

calculate the stats:

```
python calculate-stats.py
```