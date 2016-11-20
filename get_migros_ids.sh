#!/bin/bash
# Get and print the IDs of every Migros food products
# Requires curl, jq>=1.5

NB_RESULTS=1000

# get_ids <offset>
get_ids() {
	# Imitate the query sent by the browser when search on Migros' website
    # The `key` parameter seemed constant when using the search engine
	curl "https://web-api.migros.ch/widgets/product_fragments_json?region=national&q=is_variant%3Afalse&facets%5Bcategory%5D=BeSS_0101&sort=score&order=desc&facet_size=0&extra_facets%5B0%5D=category&feature_facets%5B0%5D=MAPI_VEGETARIANISM&limit=${NB_RESULTS}&key=loh7Diephiengaiv&lang=fr&offset=$1" \
		-H 'Host: web-api.migros.ch' \
		-H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0' \
		-H 'Accept: application/json, text/javascript, */*; q=0.01' \
		-H 'Accept-Language: fr' \
		-H 'Referer: https://produits.migros.ch/assortiment/supermarche/denrees-alimentaires' \
		-H 'origin: https://produits.migros.ch' \
		-H 'Connection: keep-alive' \
		-H 'Cache-Control: max-age=0' \
		--compressed \
		| jq '.[].id' -r -e
}

for page in {0..100}; do
	if ! get_ids $((${page}*${NB_RESULTS})) ; then
		break
	fi
done
