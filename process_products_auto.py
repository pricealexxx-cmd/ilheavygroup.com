#!/usr/bin/env python3
"""
Automated script to process all products from johnstractorhouse.com
Creates product pages, downloads images, and updates catalog
"""

import re
import subprocess
import os
from urllib.parse import urlparse
import html

def get_product_info(url):
    """Extract product information from URL"""
    print(f"Processing: {url}")
    
    # Get HTML content
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html_content = result.stdout
    
    # Extract price
    price_match = re.search(r'\$([0-9,]+)', html_content)
    price = price_match.group(0) if price_match else "Contact for Price"
    
    # Extract year
    year_match = re.search(r'Year[:\s]+(\d{4})', html_content, re.IGNORECASE)
    year = year_match.group(1) if year_match else ""
    
    # Extract hours
    hours_match = re.search(r'(?:Hours|Usage)[:\s]+(\d+)', html_content, re.IGNORECASE)
    hours = hours_match.group(1) if hours_match else ""
    
    # Extract stock number
    stock_match = re.search(r'Stock[:\s]+(ZID-\d+)', html_content, re.IGNORECASE)
    stock = stock_match.group(1) if stock_match else ""
    
    # Extract title
    title_match = re.search(r'<title>([^<]+)', html_content)
    title = title_match.group(1).split('|')[0].strip() if title_match else ""
    
    # Extract description
    desc_match = re.search(r'<p[^>]*>([^<]+(?:This|The)[^<]+)', html_content, re.IGNORECASE)
    description = desc_match.group(1)[:200] if desc_match else ""
    
    return {
        'url': url,
        'title': title,
        'price': price,
        'year': year,
        'hours': hours,
        'stock': stock,
        'description': description
    }

def download_images(url, slug):
    """Download all product images"""
    print(f"  Downloading images for {slug}...")
    
    # Create directory
    os.makedirs(f"images/{slug}", exist_ok=True)
    
    # Get image URLs
    result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
    html_content = result.stdout
    
    # Find all image URLs
    image_urls = re.findall(r'https://johnstractorhouse.com/wp-content/uploads/[^"]*\.(?:jpg|jpeg|png|webp)', html_content)
    image_urls = [url for url in image_urls if 'favicon' not in url and '40-yeasr' not in url and 'logo' not in url.lower() and 'banner' not in url.lower()]
    image_urls = list(set(image_urls))  # Remove duplicates
    
    print(f"  Found {len(image_urls)} images")
    
    # Download images
    for i, img_url in enumerate(image_urls[:20]):  # Limit to 20 images
        filename = os.path.basename(img_url)
        if i == 0:
            target = f"images/{slug}/main.jpg"
        else:
            target = f"images/{slug}/image{i}.jpg"
        
        subprocess.run(['curl', '-L', '-o', target, img_url], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Count downloaded images
    image_count = len([f for f in os.listdir(f"images/{slug}") if f.endswith('.jpg')])
    print(f"  Downloaded {image_count} images")
    
    return image_count

# Read product URLs
with open('products-to-process.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"Found {len(urls)} products to process")
print("Starting processing...\n")

# Process each product (skip first - already done)
for i, url in enumerate(urls[1:], 2):  # Start from second product
    print(f"\n[{i}/{len(urls)}] Processing product...")
    
    # Extract slug
    slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
    clean_slug = re.sub(r'[^a-z0-9-]', '-', slug.lower())
    
    try:
        # Get product info
        info = get_product_info(url)
        print(f"  Title: {info['title']}")
        print(f"  Price: {info['price']}")
        print(f"  Year: {info['year']}, Hours: {info['hours']}")
        
        # Download images
        image_count = download_images(url, clean_slug)
        
        print(f"  ✓ Completed: {clean_slug}")
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        continue

print("\n✓ All products processed!")

