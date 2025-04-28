from PIL import Image, ImageDraw
import os

def create_icon(name, size, draw_function):
    """Create an icon with the given name and size"""
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw_function(draw, size)
    return image

def draw_pos_icon(draw, size):
    """Draw the main POS system icon"""
    # Main rectangle
    draw.rectangle([size//8, size//6, 7*size//8, 5*size//6], fill='#007bff', outline='#0056b3', width=2)
    # Display area
    draw.rectangle([size//6, size//4, 5*size//6, size//2], fill='white', outline='#0056b3', width=1)
    # Keypad area
    draw.rectangle([size//6, 5*size//8, 5*size//6, 3*size//4], fill='white', outline='#0056b3', width=1)

def draw_dashboard_icon(draw, size):
    """Draw the dashboard icon"""
    margin = size//8
    box_size = (size - 3*margin)//2
    # Draw four boxes
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545']
    positions = [(margin, margin), (2*margin + box_size, margin),
                (margin, 2*margin + box_size), (2*margin + box_size, 2*margin + box_size)]
    
    for pos, color in zip(positions, colors):
        draw.rectangle([pos[0], pos[1], pos[0] + box_size, pos[1] + box_size],
                      fill=color, outline='white', width=1)

def draw_sales_icon(draw, size):
    """Draw the sales icon"""
    # Receipt
    draw.rectangle([size//4, size//6, 3*size//4, 5*size//6], fill='#007bff', outline='white', width=2)
    # Lines
    for y in range(size//3, 2*size//3, size//8):
        draw.line([(size//3, y), (2*size//3, y)], fill='white', width=2)

def draw_products_icon(draw, size):
    """Draw the products icon"""
    # Box
    points = [(size//2, size//6), (5*size//6, size//2), (size//2, 5*size//6), (size//6, size//2)]
    draw.polygon(points, fill='#007bff', outline='white', width=2)

def draw_categories_icon(draw, size):
    """Draw the categories icon"""
    margin = size//6
    box_size = (size - 3*margin)//2
    for x in range(2):
        for y in range(2):
            pos_x = margin + x*(margin + box_size)
            pos_y = margin + y*(margin + box_size)
            draw.rectangle([pos_x, pos_y, pos_x + box_size, pos_y + box_size],
                         fill='#007bff', outline='white', width=1)

def draw_reports_icon(draw, size):
    """Draw the reports icon"""
    # Paper
    draw.rectangle([size//6, size//6, 5*size//6, 5*size//6], fill='#007bff', outline='white', width=2)
    # Graph lines
    points = [(size//3, 2*size//3), (size//2, size//3), (2*size//3, size//2)]
    draw.line(points, fill='white', width=2)

def generate_icons():
    """Generate all icons"""
    icons = {
        'pos_icon': draw_pos_icon,
        'dashboard': draw_dashboard_icon,
        'sales': draw_sales_icon,
        'products': draw_products_icon,
        'categories': draw_categories_icon,
        'reports': draw_reports_icon
    }
    
    # Ensure the images directory exists
    image_dir = os.path.join('resources', 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # Generate icons in different sizes
    sizes = {
        'pos_icon': 64,  # Main application icon
        'dashboard': 32,  # Tab icons
        'sales': 32,
        'products': 32,
        'categories': 32,
        'reports': 32
    }
    
    for name, draw_func in icons.items():
        size = sizes[name]
        icon = create_icon(name, size, draw_func)
        icon.save(os.path.join(image_dir, f'{name}.png'))
        print(f"Generated {name}.png")

if __name__ == "__main__":
    generate_icons() 