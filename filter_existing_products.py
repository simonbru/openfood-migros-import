#!/usr/bin/env python3
"""Check which migros food products already exist in OpenFood database

Requires psycopg2 library to access the postgres database
"""

import csv
import itertools
import json
import sys
from pathlib import Path

import psycopg2

DATABASE = 'openfood_hackathon'
MIGROS_FILES_PATH = 'infofiles/'


def migros_products():
    for file in Path(MIGROS_FILES_PATH).glob('*.json'):
        migros_id = file.name.split('.')[0]
        yield migros_id, json.loads(file.read_text())


class InvalidProductError(Exception):
    pass


def product_exists_in_openfood(cursor, product):
    try:
        barcodes = product['_source']['eans']
    except KeyError:
        raise InvalidProductError("Couldn't access barcodes field in product")

    if not barcodes:
        raise InvalidProductError("Empty barcodes field in product")

    cursor.execute(
        'SELECT 1 FROM products WHERE barcode IN %s',
        (tuple(barcodes),)
    )
    return cursor.rowcount == 1


def csv_output(output_file, cur, products):
    writer = csv.writer(output_file)
    writer.writerow(['name', 'state', 'migros_id', 'barcode in OpenFood', 'other barcodes'])
    for product_id, product in itertools.islice(products, 100):
        try:
            if not product_exists_in_openfood(cur, product):
                writer.writerow((
                    product['title'], 'present', product_id, ' ', ','.join(product['_source']['eans'])
                ))
            else:
                writer.writerow((
                    product['title'], 'missing', product_id, ' ', ','.join(product['_source']['eans'])
                ))
        except InvalidProductError as e:
            print("Error parsing migros product {}: {}".format(product_id, e))


def main():
    conn = psycopg2.connect(database=DATABASE)
    cur = conn.cursor()
    if len(sys.argv) == 3 and sys.argv[1] == '--csv':
        with open(sys.argv[2], 'w') as f:
            csv_output(f, cur, migros_products())
    else:
        for product_id, product in migros_products():
            try:
                if not product_exists_in_openfood(cur, product):
                    print("missing: " + product_id)
                else:
                    print("ok: " + product_id)
            except InvalidProductError as e:
                print("Error parsing migros product {}: {}".format(product_id, e))


if __name__ == '__main__':
    main()
