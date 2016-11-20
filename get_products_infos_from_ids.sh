#!/bin/bash
# Get migros products ids from stdin and save json dumps of products
# in infofiles/ folder

split_info() {
	local result="$(retrieve_product $1)"
	jq <<<"$result" '.results[0]'
}

# retrieve_product <migros_product_id>
retrieve_product() {
    # Add _source=true parameter to retrieve additionnal information from
    # Migros' backend. We need it to gather the barcodes. This may not work in
    # the future.
	curl "https://search-api.migros.ch/products?lang=fr&key=migros_components_search&limit=10&offset=0&q=$1&_source=true" \
        -H 'Host: search-api.migros.ch' \
        -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0' \
        -H 'Accept: application/json, text/javascript, */*; q=0.01' \
        -H 'Referer: https://search.migros.ch/fr/' \
        -H 'Origin: https://search.migros.ch' \
        --compressed
}

retrieve_all_products() {
	while read migros_id; do
        local fpath="infofiles/${migros_id}.json"
        # Skip products already retrieved
		if [ ! -e "$fpath" ]; then
			split_info $migros_id > "$fpath"
		else
			echo "$fpath" already retrieved
		fi
	done
}

retrieve_all_products
