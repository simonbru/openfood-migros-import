#!/usr/bin/env python3
"""Check which migros food products already exist in OpenFood database

Requires psycopg2 library to access the postgres database
"""

import json
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


def main():
    conn = psycopg2.connect(database=DATABASE)
    cur = conn.cursor()
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
