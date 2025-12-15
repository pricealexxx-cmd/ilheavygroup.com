#!/usr/bin/env python3
"""
Fix remaining issues in product pages - remove duplicates and fix descriptions
"""

import re
import subprocess
import os

def extract_product_info(url):
    """Extract product information"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    # Title
    title_match = re.search(r'<title>([^<]+)', html)
    title = title_match.group(1).split('|')[0].strip() if title_match else ""
    title = title.replace('&#8212;', '-').replace('&amp;', '&').replace('&#8217;', "'")
    
    # Year
    year = ""
    for pattern in [
        r'<li><span>Year:</span>\s*(\d{4})',
        r'Year[:\s]+(\d{4})',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            year = match.group(1)
            break
    
    # Hours
    hours = ""
    for pattern in [
        r'<li><span>(?:Hours|Usage):</span>\s*([0-9,]+)',
        r'(?:Hours|Usage)[:\s]+([0-9,]+)',
    ]:
        match = re.search(pattern, html, re.I)
        if match:
            hours = match.group(1).replace(',', '')
            break
    
    # Get first part of title for description
    words = title.split()
    if len(words) >= 2:
        model_name = words[0] + ' ' + words[1]
    else:
        model_name = title
    
    return {
        'title': title,
        'year': year,
        'hours': hours,
        'model_name': model_name
    }

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print("Fixing remaining issues in product pages...\n")

for i, url in enumerate(urls, 1):
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    filename = f"product-{clean_slug}.html"
    if not os.path.exists(filename):
        continue
    
    try:
        info = extract_product_info(url)
        
        with open(filename, 'r') as f:
            content = f.read()
        
        # Fix duplicate hours in Quick Details
        content = re.sub(r'<li>✓ <strong>Hours: (\d+)</strong> \d+</li>', 
                        r'<li>✓ <strong>Hours: \1</strong></li>', content)
        
        # Fix description - replace old template text
        old_desc_pattern = r'The <strong>\d{4} [A-Z]+</strong> is a powerful'
        new_desc = f'The <strong>{info["year"]} {info["model_name"]}</strong> is a powerful'
        content = re.sub(old_desc_pattern, new_desc, content)
        
        # Fix description at bottom
        old_bottom = r'This \d{4} \d{4} [A-Z]+ track loader'
        new_bottom = f'This {info["year"]} {info["model_name"]}'
        content = re.sub(old_bottom, new_bottom, content)
        
        # Fix contact link
        content = re.sub(r'contact\.html\?product=[^"]+', 
                        f'contact.html?product={info["model_name"].replace(" ", "%20")}', content)
        
        # Fix manufacturer in Quick Details
        if 'John Deere' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> John Deere</li>', content)
        elif 'Caterpillar' in info['title'] or 'CAT' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> Caterpillar</li>', content)
        elif 'Bobcat' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> Bobcat</li>', content)
        elif 'Kubota' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> Kubota</li>', content)
        elif 'JLG' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> JLG</li>', content)
        elif 'JCB' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> JCB</li>', content)
        elif 'Peterbilt' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> Peterbilt</li>', content)
        elif 'Kenworth' in info['title']:
            content = re.sub(r'<li>✓ <strong>Manufacturer:</strong> [^<]+</li>',
                           '<li>✓ <strong>Manufacturer:</strong> Kenworth</li>', content)
        
        # Fix type based on title
        if 'Tractor' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Tractor</li>', content)
        elif 'Backhoe' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Backhoe Loader</li>', content)
        elif 'Telehandler' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Telehandler</li>', content)
        elif 'Dump Truck' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Dump Truck</li>', content)
        elif 'Motor Grader' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Motor Grader</li>', content)
        elif 'Excavator' in info['title'] or 'Mini Excavator' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Excavator</li>', content)
        elif 'Skid Steer' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Skid Steer Loader</li>', content)
        elif 'Track Loader' in info['title']:
            content = re.sub(r'<li>✓ <strong>Type:</strong> [^<]+</li>',
                           '<li>✓ <strong>Type:</strong> Compact Track Loader</li>', content)
        
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"[{i}/{len(urls)}] ✓ {clean_slug}")
        
    except Exception as e:
        print(f"[{i}/{len(urls)}] ✗ {clean_slug} - Error: {e}")

print("\n✓ All issues fixed!")










