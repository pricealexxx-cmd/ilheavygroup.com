#!/usr/bin/env python3
"""
Simple fix for all N/A values - direct replacement
"""

import re
import subprocess

def get_product_data():
    """Get all product data"""
    products = {}
    
    with open('products-to-process.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    for url in urls:
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        html = result.stdout
        
        slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
        clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
        if 'caterpillar-299d3' in url:
            clean_slug = 'caterpillar-299d3-2022'
        
        year = ""
        year_match = re.search(r'Year[:\s]+(\d{4})', html, re.IGNORECASE)
        if year_match:
            year = year_match.group(1)
        
        hours = ""
        hours_match = re.search(r'(?:Hours|Usage)[:\s]+(\d+)', html, re.IGNORECASE)
        if hours_match:
            hours = hours_match.group(1)
        
        products[clean_slug] = {'year': year, 'hours': hours}
    
    return products

products = get_product_data()

# Fix index.html
print("Fixing index.html...")
with open('index.html', 'r') as f:
    content = f.read()

for slug, info in products.items():
    if info['year']:
        # Replace N/A after product link
        pattern = f'product-{re.escape(slug)}\\.html[^>]*>.*?<span><strong>Year:</strong>\\s*N/A'
        replacement = f'product-{slug}.html" class="btn btn-secondary">Details</a>\n                        </div>\n                    </div>\n\n                    <div class="product-card">\n                        <div class="product-image">\n                            <img src="images/{slug}/main.jpg" alt="{slug}">\n                            <div style="position: absolute; top: 10px; right: 10px; background: var(--primary-color); color: white; padding: 0.5rem 1rem; border-radius: 5px; font-weight: 600; font-size: 0.9rem;">Used</div>\n                        </div>\n                        <div class="product-content">\n                            <h3>{slug}</h3>\n                            <p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">$Price</p>\n                            <p>{slug} - Premium equipment ready for work.</p>\n                            <div class="product-specs">\n                                <span><strong>Year:</strong> {info["year"]}'
        # Simple replacement
        content = content.replace(
            f'href="product-{slug}.html" class="btn btn-secondary">Details</a>\n                        </div>\n                    </div>\n\n                    <div class="product-card">\n                        <div class="product-image">\n                            <img src="images/{slug}/main.jpg" alt="{slug}">\n                            <div style="position: absolute; top: 10px; right: 10px; background: var(--primary-color); color: white; padding: 0.5rem 1rem; border-radius: 5px; font-weight: 600; font-size: 0.9rem;">Used</div>\n                        </div>\n                        <div class="product-content">\n                            <h3>{slug}</h3>\n                            <p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">$Price</p>\n                            <p>{slug} - Premium equipment ready for work.</p>\n                            <div class="product-specs">\n                                <span><strong>Year:</strong> N/A',
            f'href="product-{slug}.html" class="btn btn-secondary">Details</a>\n                        </div>\n                    </div>\n\n                    <div class="product-card">\n                        <div class="product-image">\n                            <img src="images/{slug}/main.jpg" alt="{slug}">\n                            <div style="position: absolute; top: 10px; right: 10px; background: var(--primary-color); color: white; padding: 0.5rem 1rem; border-radius: 5px; font-weight: 600; font-size: 0.9rem;">Used</div>\n                        </div>\n                        <div class="product-content">\n                            <h3>{slug}</h3>\n                            <p style="color: var(--primary-color); font-weight: 600; font-size: 1.1rem; margin: 0.5rem 0;">$Price</p>\n                            <p>{slug} - Premium equipment ready for work.</p>\n                            <div class="product-specs">\n                                <span><strong>Year:</strong> {info["year"]}'
        )
    
    if info['hours']:
        content = content.replace(
            f'<span><strong>Hours:</strong> N/A</span>\n                            </div>\n                            <a href="product-{slug}.html"',
            f'<span><strong>Hours:</strong> {info["hours"]}</span>\n                            </div>\n                            <a href="product-{slug}.html"'
        )

with open('index.html', 'w') as f:
    f.write(content)

print("✓ Done")










