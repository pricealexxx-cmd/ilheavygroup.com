#!/usr/bin/env python3
"""
Script to process products from johnstractorhouse.com
Downloads images, creates product pages, and adds to catalog
"""

import re
import subprocess
import os
from urllib.parse import urlparse

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Found {len(urls)} products to process")

# Process first 3 products as test
for i, url in enumerate(urls[:3], 1):
    print(f"\n[{i}/{len(urls)}] Processing: {url}")
    
    # Extract product name from URL
    product_slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    print(f"  Product slug: {product_slug}")

