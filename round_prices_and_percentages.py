#!/usr/bin/env python3
"""
Round discount prices to nearest $100 and percentages to whole numbers
"""

import re
import os

def round_to_100(price_str):
    """Round price to nearest $100"""
    # Extract number
    num_str = price_str.replace('$', '').replace(',', '')
    try:
        num = int(num_str)
        # Round to nearest 100
        rounded = round(num / 100) * 100
        return f"${rounded:,}"
    except:
        return price_str

def round_percentage(percent):
    """Round percentage to whole number"""
    try:
        return round(float(percent))
    except:
        return percent

print("Rounding prices and percentages...\n")

# Update index.html
with open('index.html', 'r') as f:
    content = f.read()

# Find all discount prices and round them
# Pattern: <span style="color: #dc2626; font-weight: 700;">$XX,XXX</span> <span style="background: #dc2626...">-XX.X%</span>
def round_price_in_match(m):
    price = m.group(1)
    percent = m.group(2)
    rounded_price = round_to_100(price)
    rounded_percent = round_percentage(percent)
    return f'<span style="color: #dc2626; font-weight: 700;">{rounded_price}</span> <span style="background: #dc2626; color: white; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85em; font-weight: 600; margin-left: 0.5rem;">-{rounded_percent}%</span>'

content = re.sub(
    r'<span style="color: #dc2626; font-weight: 700;">(\$[0-9,]+)</span> <span style="background: #dc2626[^>]*>(-[0-9.]+)%</span>',
    round_price_in_match,
    content
)

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Updated index.html\n")

# Update catalog.html
with open('catalog.html', 'r') as f:
    content = f.read()

content = re.sub(
    r'<span style="color: #dc2626; font-weight: 700;">(\$[0-9,]+)</span> <span style="background: #dc2626[^>]*>(-[0-9.]+)%</span>',
    round_price_in_match,
    content
)

with open('catalog.html', 'w') as f:
    f.write(content)

print("✓ Updated catalog.html\n")

# Update product pages
print("Updating product pages...")
for filename in os.listdir('.'):
    if filename.startswith('product-') and filename.endswith('.html'):
        # Skip Bobcat products
        if 'bobcat' in filename.lower():
            continue
        
        with open(filename, 'r') as f:
            content = f.read()
        
        # Round prices in price badge
        def round_price_badge(m):
            old_price = m.group(1)
            new_price = m.group(2)
            percent = m.group(3)
            rounded_new = round_to_100(new_price)
            rounded_percent = round_percentage(percent)
            return f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{old_price} USD</span><span style="color: #dc2626; font-weight: 700; font-size: 1.2em;">{rounded_new} USD</span><div style="background: #dc2626; color: white; padding: 0.5rem 1rem; border-radius: 5px; display: inline-block; margin-left: 1rem; font-weight: 600; font-size: 0.9em;">Save {rounded_percent}%</div>'
        
        content = re.sub(
            r'<span style="text-decoration: line-through; color: #999; font-size: 0\.9em; margin-right: 0\.5rem;">(\$[0-9,]+) USD</span><span style="color: #dc2626; font-weight: 700; font-size: 1\.2em;">(\$[0-9,]+) USD</span><div style="background: #dc2626[^>]*>Save ([0-9.]+)%</div>',
            round_price_badge,
            content
        )
        
        # Also round in paragraphs
        content = re.sub(
            r'<span style="color: #dc2626; font-weight: 700;">(\$[0-9,]+)</span> <span style="background: #dc2626[^>]*>(-[0-9.]+)%</span>',
            round_price_in_match,
            content
        )
        
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"  ✓ Updated {filename}")

print("\n✓ All prices rounded to nearest $100")
print("✓ All percentages rounded to whole numbers")





