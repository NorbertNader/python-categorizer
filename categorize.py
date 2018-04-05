"""This module associates purchases to specific buckets and outputs them to a json file.

"""

import json
import csv

class Categorize:
    """Class for cateogirzing purchases.

    This class is used to parse purchase history and assign each purchase to a specific bucket.
    We provide the class with paths to the purchases and baskets files.
    Then we create a json object with buckets, then we assign the purchases to the buckets
    that the script will assign them to.

    TODO:
     - add exceptions when handeling files
    """

    categorized_data = []
    purchases_csv = 'inputdata/purchase_data.csv'
    buckets_csv = 'inputdata/purchase_buckets.csv'
    bucket_dict_index = {}

    def __init__(self):
        """Initial function

        The init will append the wildcard bucket that will receive all uncategorizable purchases.

        """
        self.categorized_data.append({
            'bucket': '*,*,*',
            'purchases': []
        })
        self.bucket_dict_index['*,*,*'] = 0

    def run(self):
        """Function that creates the categorized object

        """
        self.__read_buckets()
        self.__read_purchases()

    def __read_buckets(self):
        """Function that will parse the buckets csv and append them to the global json data object.

        """
        with open(self.buckets_csv, 'r') as buckets:
            buckets_rows = csv.reader(buckets, delimiter=',')
            self.__append_buckets(buckets_rows)

    def __append_buckets(self, buckets_rows):
        """Function that will append buckets to categorized_data without duplicates
           Args:
            - buckets_rows {list} - unfiltered buckets from csv
        """
        # this index will help us find the basket
        current_index = 0

        for row in buckets_rows:
            # crate string from row to create index key
            row_string = ','.join(row)

            # if bucket already indexed continue
            if row_string in self.bucket_dict_index:
                continue

            # index bucket (increment because we added widlcard on init)
            current_index += 1

            self.bucket_dict_index[row_string.lower()] = current_index

            # append the bucket to the json object
            self.categorized_data.append({
                'bucket': ','.join(row),
                'purchases': []
            })


    def __read_purchases(self):
        """Function that will parse the purchases csv and add them to the categorized data object.

        """
        with open(self.purchases_csv, 'r') as purchases:
            purchases_rows = csv.reader(purchases, delimiter=',')
            self.__append_purchases(purchases_rows)

    def __append_purchases(self, purchases_rows):
        """Function that will append purchases to appropriate basket.
           Args:
            - purchases_rows {list} - all purchases from csv
        """
        for row in purchases_rows:
            best_match = 0
            purchase_publisher = row[2].lower()
            purchase_duration = row[5]
            purchase_price = row[4]
            score = 0

            for bucket in self.bucket_dict_index:
                bucket_set = bucket.split(',')
                wildcard = {
                    'publisher': bucket_set[0].lower() == '*',
                    'duration': bucket_set[2] == '*',
                    'price': bucket_set[1] == '*'
                }
                matches = {
                    'publisher': purchase_publisher.lower() == bucket_set[0].lower(),
                    'duration': purchase_duration == bucket_set[2],
                    'price': purchase_price == bucket_set[1]
                }

                if matches['publisher'] and matches['duration'] and matches['price']:
                    best_match = self.bucket_dict_index[bucket]
                    break

                if matches['publisher'] and matches['duration'] and wildcard['price']:
                    if score < 6:
                        score = 6
                        best_match = self.bucket_dict_index[bucket]
                        continue

                if matches['publisher'] and wildcard['duration'] and matches['price']:
                    if score < 5:
                        score = 5
                        best_match = self.bucket_dict_index[bucket]
                        continue

                if matches['publisher'] and wildcard['duration'] and wildcard['price']:
                    if score < 4:
                        score = 4
                        best_match = self.bucket_dict_index[bucket]
                        continue

                if wildcard['publisher'] and matches['duration'] and matches['price']:
                    if score < 3:
                        score = 3
                        best_match = self.bucket_dict_index[bucket]
                        continue

                if wildcard['publisher'] and matches['duration'] and wildcard['price']:
                    if score < 2:
                        score = 2
                        best_match = self.bucket_dict_index[bucket]
                        continue

                if wildcard['publisher'] and wildcard['duration'] and matches['price']:
                    if score == 0:
                        score = 1
                        best_match = self.bucket_dict_index[bucket]
                        continue

            self.categorized_data[best_match]['purchases'].append(','.join(row))

    def output_json(self):
        """Function that will output json file with the categorized purchases.

        """
        with open('outputdata/categorized-purchases.json', 'w') as json_output:
            json.dump(self.categorized_data, json_output, indent=4)
