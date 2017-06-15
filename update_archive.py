#!/usr/bin/env python3

from pyFCC.archive import get_attachment_urls, parse_fcc_id, load_next, fetch_and_pack#, errorFunction
from pyFCC.fccDB import create_product_table, populate_products
import sys

if __name__ == '__main__':
	if len(sys.argv) <2:
		print("Usage: archive.py <FCC id>")
		sys.exit(1)
	for fcc_id in sys.argv[1:]:
		print("Looking up FCC id: %s" % fcc_id)
		product_data = load_next(fcc_id)
		
		for key, value in product_data.items():
			for row in value:			
				print("Fetching result %d" % row['version'])
				attachments = get_attachment_urls(row['url'])

				if attachments:
					dir_name = "%s/%s/%d" % (row['grantee_code'], row['product_code'], row['version'])
					fetch_and_pack(attachments, dir_name, row['url'])

	create_product_table()
	populate_products(product_data)

