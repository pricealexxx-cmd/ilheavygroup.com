#!/usr/bin/env python3
"""
Remove duplicate product cards from index.html
"""

import re

with open('index.html', 'r') as f:
    content = f.read()

# Find all product cards
product_cards = re.findall(r'(<div class="product-card">.*?</div>\s*</div>\s*</div>)', content, re.DOTALL)

# Track seen slugs
seen_slugs = {}
duplicates = []

for i, card in enumerate(product_cards):
    # Extract slug
    slug_match = re.search(r'href="product-([^"]+\.html)"', card)
    if slug_match:
        slug = slug_match.group(1).replace('.html', '')
        
        if slug in seen_slugs:
            # This is a duplicate
            duplicates.append((slug, card))
            print(f"Found duplicate: {slug}")
        else:
            seen_slugs[slug] = card

print(f"\nFound {len(duplicates)} duplicate product cards")

# Remove duplicates (keep first occurrence)
for slug, duplicate_card in duplicates:
    # Remove the duplicate (but be careful - only remove if it's exactly the same)
    # We'll remove the second occurrence
    content = content.replace(duplicate_card, '', 1)  # Remove only first occurrence of duplicate

# Clean up any extra blank lines
content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Duplicates removed!")










