#!/usr/bin/env python3
"""
Fix price display - ensure old price is strikethrough gray, new price is highlighted red
"""

import re
import os

# Product discounts (from previous run)
product_discounts = {
    'caterpillar-299d3-2022': {'original': '$50,300', 'new': '$41,592', 'discount': 17.3},
    '2021-bobcat-t870-skid-steer-track': {'original': '$48,500', 'new': '$40,174', 'discount': 17.2},
    '2018-caterpillar-320gc': {'original': '$74,700', 'new': '$60,750', 'discount': 18.7},
    '2018-caterpillar-420f2-backhoe': {'original': '$50,000', 'new': '$42,202', 'discount': 15.6},
    '2023-john-deere-770gp-motor-grader': {'original': '$197,000', 'new': '$161,140', 'discount': 18.2},
    '2015-caterpillar-backhoe-loader-420f2-it': {'original': '$45,200', 'new': '$37,222', 'discount': 17.6},
    '2019-caterpillar-313flgc': {'original': '$63,100', 'new': '$51,401', 'discount': 18.5},
    '2018-caterpillar-320': {'original': '$80,300', 'new': '$68,106', 'discount': 15.2},
    '2019-caterpillar-312f': {'original': '$51,000', 'new': '$43,291', 'discount': 15.1},
    '2017-caterpillar-excavator-316fl': {'original': '$55,400', 'new': '$45,355', 'discount': 18.1},
    '2021-kubota-u55-5-mini-excavator': {'original': '$40,500', 'new': '$32,649', 'discount': 19.4},
    '2022-kubota-u50-5-mini-excavator': {'original': '$35,900', 'new': '$28,853', 'discount': 19.6},
    '2021-kubota-u48-5-mini-excavator': {'original': '$43,600', 'new': '$35,361', 'discount': 18.9},
    '2022-kubota-kx-040-4-mini-excavator': {'original': '$40,300', 'new': '$33,558', 'discount': 16.7},
    '2024-bobcat-t86-compact-track-loader': {'original': '$47,100', 'new': '$38,277', 'discount': 18.7},
    '2024-kubota-svl97-2hfc-compact-track-loader': {'original': '$44,900', 'new': '$36,133', 'discount': 19.5},
    '2024-kubota-svl97-2-compact-track-loader': {'original': '$41,800', 'new': '$35,195', 'discount': 15.8},
    '2020-kubota-svl95-2shfc-compact-track-loader': {'original': '$35,100', 'new': '$28,480', 'discount': 18.9},
    '2022-caterpillar-259d3-skid-steer-loader': {'original': '$46,500', 'new': '$38,846', 'discount': 16.5},
    'deere-331g-skid-steer-track': {'original': '$44,900', 'new': '$37,146', 'discount': 17.3},
    '2022-caterpillar-skid-steer-259d3': {'original': '$48,500', 'new': '$39,392', 'discount': 18.8},
    '2019-kubota-svl75-2-skid-steer': {'original': '$38,500', 'new': '$32,347', 'discount': 16.0},
    '2023-bobcat-t770-track-skid-steer': {'original': '$41,000', 'new': '$33,068', 'discount': 19.3},
    '2019-john-deere-8245r-tractor': {'original': '$91,800', 'new': '$77,519', 'discount': 15.6},
    '2019-caterpillar-tl1255d-telehandler': {'original': '$50,000', 'new': '$42,186', 'discount': 15.6},
    '2022-jlg-925-telehandler': {'original': '$51,400', 'new': '$42,275', 'discount': 17.8},
    '2023-jcb-510-56-telehandler-2': {'original': '$49,500', 'new': '$39,710', 'discount': 19.8},
    '2023-caterpillar-tl1055-telehandler': {'original': '$70,500', 'new': '$57,589', 'discount': 18.3},
    '2022-kenworth-t880-quad-axle-dump-truck': {'original': '$101,100', 'new': '$83,916', 'discount': 17.0},
    '2020-peterbilt-389-tri-axle-dump-truck': {'original': '$62,600', 'new': '$51,043', 'discount': 18.5},
    '2019-peterbilt-389-tri-axle-dump-truck': {'original': '$74,200', 'new': '$60,901', 'discount': 17.9},
}

print("Fixing price display on product pages...\n")

# Fix product pages
for slug, prices in product_discounts.items():
    filename = f"product-{slug}.html"
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Fix price badge - remove duplicates and fix format
    old_price_html = f'<span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{prices["original"]} USD</span><span style="color: #dc2626; font-weight: 700; font-size: 1.2em;">{prices["new"]} USD</span><div style="background: #dc2626; color: white; padding: 0.5rem 1rem; border-radius: 5px; display: inline-block; margin-left: 1rem; font-weight: 600; font-size: 0.9em;">Save {prices["discount"]}%</div>'
    
    # Replace any existing price badge
    content = re.sub(r'<div class="price-badge">.*?</div>', f'<div class="price-badge">{old_price_html}</div>', content, flags=re.DOTALL)
    
    # Also fix any price in paragraphs
    content = re.sub(
        rf'<p[^>]*style="[^"]*color[^"]*var\\(--primary-color\\)[^"]*"[^>]*>.*?{re.escape(prices["original"])}.*?</p>',
        f'<p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;"><span style="text-decoration: line-through; color: #999; font-size: 0.9em; margin-right: 0.5rem;">{prices["original"]}</span><span style="color: #dc2626; font-weight: 700;">{prices["new"]}</span></p>',
        content,
        flags=re.DOTALL
    )
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Fixed {filename}")

print("\n✓ All product pages fixed!")





