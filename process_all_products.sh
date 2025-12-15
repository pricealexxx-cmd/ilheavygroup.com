#!/bin/bash

# Script to process all products from johnstractorhouse.com
# Downloads images, creates product pages, and adds to catalog

PRODUCTS_FILE="products-to-process.txt"
BASE_URL="https://johnstractorhouse.com/equipment/"

# Skip first product (already processed)
tail -n +2 "$PRODUCTS_FILE" | while read url; do
    if [ -z "$url" ]; then continue; fi
    
    # Extract product slug
    slug=$(echo "$url" | sed 's|.*equipment/||;s|/$||')
    clean_slug=$(echo "$slug" | tr '/' '_' | tr ' ' '_' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_-]//g')
    
    echo "Processing: $slug"
    echo "Clean slug: $clean_slug"
    
    # Create directory
    mkdir -p "images/$clean_slug"
    
    # Download images (excluding logos/banners)
    cd "images/$clean_slug"
    curl -s "$url" | grep -oE 'https://johnstractorhouse.com/wp-content/uploads/[^"]*\.(jpg|jpeg|png|webp)' | \
        grep -v favicon | grep -v "40-yeasr\|40-year\|logo\|banner" | sort -u | \
        while read img_url; do
            filename=$(basename "$img_url")
            curl -L -o "$filename" "$img_url" 2>/dev/null
        done
    
    # Rename first image to main.jpg, rest to image1.jpg, image2.jpg, etc.
    counter=1
    for file in *.jpg *.jpeg *.png *.webp 2>/dev/null; do
        if [ -f "$file" ]; then
            if [ $counter -eq 1 ]; then
                mv "$file" "main.jpg" 2>/dev/null
            else
                mv "$file" "image$((counter-1)).jpg" 2>/dev/null
            fi
            counter=$((counter+1))
        fi
    done
    
    cd ../../..
    echo "✓ Completed: $slug"
    echo ""
done

echo "All products processed!"










