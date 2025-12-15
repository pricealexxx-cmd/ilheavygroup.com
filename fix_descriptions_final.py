#!/usr/bin/env python3
"""
Fix descriptions in all product pages with correct model names
"""

import re
import subprocess
import os

def extract_full_title(url):
    """Extract full product title"""
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html = result.stdout
    
    # Get title
    title_match = re.search(r'<title>([^<]+)', html)
    if title_match:
        title = title_match.group(1).split('|')[0].strip()
        title = title.replace('&#8212;', '-').replace('&amp;', '&').replace('&#8217;', "'")
        return title
    
    # Fallback - extract from h1
    h1_match = re.search(r'<h1[^>]*>([^<]+)', html)
    if h1_match:
        return h1_match.group(1).strip()
    
    return ""

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print("Fixing descriptions with correct model names...\n")

for i, url in enumerate(urls, 1):
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    if 'caterpillar-299d3' in url:
        clean_slug = 'caterpillar-299d3-2022'
    
    filename = f"product-{clean_slug}.html"
    if not os.path.exists(filename):
        continue
    
    try:
        full_title = extract_full_title(url)
        if not full_title:
            print(f"[{i}/{len(urls)}] ⚠ {clean_slug} - No title found")
            continue
        
        # Extract year and model
        year_match = re.search(r'(\d{4})', full_title)
        year = year_match.group(1) if year_match else ""
        
        # Get model name (everything after year)
        model_parts = full_title.split()
        if year and year in model_parts:
            idx = model_parts.index(year)
            model_name = ' '.join(model_parts[idx:])
        else:
            model_name = full_title
        
        with open(filename, 'r') as f:
            content = f.read()
        
        # Fix description - replace incorrect model names
        # Pattern: "The <strong>YEAR YEAR MODEL" -> "The <strong>YEAR MODEL"
        content = re.sub(r'The <strong>(\d{4}) \d{4} ([^<]+)</strong>', 
                        f'The <strong>{year} {model_name}</strong>', content)
        
        # Also fix if it's just "YEAR MODEL" without duplicate
        content = re.sub(r'The <strong>(\d{4}) ([A-Z][a-z]+)</strong> is a powerful',
                        f'The <strong>{year} {model_name}</strong> is a powerful', content)
        
        # Fix bottom description
        content = re.sub(r'This \d{4} \d{4} [^<]+ track loader',
                        f'This {year} {model_name}', content)
        content = re.sub(r'This \d{4} [A-Z][a-z]+ track loader',
                        f'This {year} {model_name}', content)
        
        # Fix h1 title if needed
        old_h1 = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
        if old_h1 and 'CATERPILLAR' in old_h1.group(1) and 'Caterpillar' not in model_name:
            content = re.sub(r'<h1[^>]*>[^<]+</h1>', f'<h1>{full_title}</h1>', content, count=1)
        
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"[{i}/{len(urls)}] ✓ {clean_slug} - {model_name[:50]}")
        
    except Exception as e:
        print(f"[{i}/{len(urls)}] ✗ {clean_slug} - Error: {e}")

print("\n✓ All descriptions fixed!")










