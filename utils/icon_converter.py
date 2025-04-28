from PIL import Image
import cairosvg
import os

def convert_svg_to_png():
    """Convert all SVG icons in the resources/images directory to PNG format"""
    image_dir = os.path.join('resources', 'images')
    
    # Ensure the images directory exists
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # List of SVG files to convert
    svg_files = [
        'pos_icon.svg',
        'dashboard.svg',
        'sales.svg',
        'products.svg',
        'categories.svg',
        'reports.svg'
    ]
    
    for svg_file in svg_files:
        svg_path = os.path.join(image_dir, svg_file)
        png_path = os.path.join(image_dir, svg_file.replace('.svg', '.png'))
        
        if os.path.exists(svg_path):
            try:
                # Convert SVG to PNG
                cairosvg.svg2png(url=svg_path, write_to=png_path)
                print(f"Converted {svg_file} to PNG")
            except Exception as e:
                print(f"Error converting {svg_file}: {str(e)}")

if __name__ == "__main__":
    convert_svg_to_png() 