# openfood-migros-import

## Usage

```bash
# Get the IDs of all food products of Migros
./get_migros_ids.sh > migros_ids.txt

# Retrieve and save a JSON dump in infofiles/ for each food product
# (These contain the barcodes that we need)
./get_products_infos_from_ids.sh < migros_ids.txt

# Check which product is missing from OpenFood database (use their
# postgres database directly)
./filter_existing_products.py
```
