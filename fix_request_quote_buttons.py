#!/usr/bin/env python3
"""
Update all Request Quote buttons to use full product names
"""

import re
import os

# Map of product filenames to their full names from contact.html
# We'll extract from HTML files themselves
product_names = {}

# First, read contact.html to get all product names
with open('contact.html', 'r') as f:
    contact_content = f.read()
    
# Extract all product options
option_pattern = r'<option value="([^"]+)">([^<]+)</option>'
matches = re.findall(option_pattern, contact_content)
for value, text in matches:
    if value and value not in ['', 'Other', 'General']:
        # Use the value as the product name
        product_names[value] = value

print(f"Found {len(product_names)} products in contact.html")

# Now update all product pages
updated_count = 0

for filename in os.listdir('.'):
    if not filename.startswith('product-') or not filename.endswith('.html'):
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Extract product title from h1 or title tag
    title_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if not title_match:
        title_match = re.search(r'<title>([^<]+)</title>', content)
    
    if title_match:
        product_title = title_match.group(1).strip()
        # Clean up title (remove " - IL Heavy Group" etc)
        product_title = re.sub(r'\s*-\s*IL Heavy Group.*$', '', product_title)
        product_title = re.sub(r'\s*-\s*Premium.*$', '', product_title)
        product_title = product_title.strip()
        
        # Find the best match in product_names
        best_match = None
        product_title_lower = product_title.lower()
        
        # Try exact match first
        for name in product_names:
            if name.lower() == product_title_lower:
                best_match = name
                break
        
        # Try partial match
        if not best_match:
            for name in product_names:
                name_lower = name.lower()
                # Check if product title contains key parts of name or vice versa
                if (product_title_lower in name_lower or 
                    name_lower in product_title_lower or
                    any(word in name_lower for word in product_title_lower.split() if len(word) > 3)):
                    best_match = name
                    break
        
        if best_match:
            # URL encode the product name
            import urllib.parse
            encoded_name = urllib.parse.quote(best_match)
            
            # Replace all Request Quote links
            # Pattern: contact.html?product=...
            old_pattern = r'contact\.html\?product=[^"\'&]+'
            new_url = f'contact.html?product={encoded_name}'
            
            content = re.sub(old_pattern, new_url, content)
            
            if content != original_content:
                with open(filename, 'w') as f:
                    f.write(content)
                updated_count += 1
                print(f"✓ Updated {filename}: {product_title} -> {best_match}")
        else:
            print(f"⚠ No match found for {filename}: {product_title}")

print(f"\n✓ Updated {updated_count} product pages")

