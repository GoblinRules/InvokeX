"""
Icon Generator for InvokeX
Creates a simple .ico file for the InvokeX application

Requirements: Pillow (PIL)
Install with: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_invokex_icon():
        """Create a simple InvokeX icon with a modern design."""
        
        # Create a 256x256 image with a dark background
        size = 256
        img = Image.new('RGBA', (size, size), (30, 30, 30, 255))
        draw = ImageDraw.Draw(img)
        
        # Create a modern, tech-inspired design
        # Outer circle
        margin = 20
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    outline=(0, 150, 255, 255), width=8)
        
        # Inner circle
        inner_margin = 50
        draw.ellipse([inner_margin, inner_margin, size-inner_margin, size-inner_margin], 
                    fill=(0, 150, 255, 100), outline=(0, 150, 255, 255), width=4)
        
        # Center X symbol
        x_margin = 80
        x_width = 8
        # Draw X lines
        draw.line([(x_margin, x_margin), (size-x_margin, size-x_margin)], 
                 fill=(255, 255, 255, 255), width=x_width)
        draw.line([(size-x_margin, x_margin), (x_margin, size-x_margin)], 
                 fill=(255, 255, 255, 255), width=x_width)
        
        # Add some tech details
        # Small circles around the edge
        for i in range(8):
            angle = i * 45
            x = size//2 + int(90 * (angle * 3.14159 / 180))
            y = size//2 + int(90 * (angle * 3.14159 / 180))
            draw.ellipse([x-3, y-3, x+3, y+3], fill=(0, 200, 255, 255))
        
        # Save as ICO
        icon_sizes = [16, 32, 48, 64, 128, 256]
        images = []
        
        for icon_size in icon_sizes:
            resized = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
            images.append(resized)
        
        # Save the icon
        img.save('icon.ico', format='ICO', sizes=[(size, size) for size in icon_sizes])
        print(f"✓ InvokeX icon created successfully: icon.ico")
        print(f"  Icon includes sizes: {', '.join(map(str, icon_sizes))}")
        
    if __name__ == "__main__":
        create_invokex_icon()
        
except ImportError:
    print("Pillow (PIL) not found. Installing...")
    import subprocess
    import sys
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        print("Pillow installed successfully. Please run this script again.")
    except subprocess.CalledProcessError:
        print("Failed to install Pillow. Please install manually:")
        print("pip install Pillow")
        
except Exception as e:
    print(f"Error creating icon: {e}")
    print("Creating a simple placeholder icon...")
    
    # Create a simple text-based icon as fallback
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple 256x256 icon
        img = Image.new('RGBA', (256, 256), (30, 30, 30, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple X
        draw.line([(50, 50), (206, 206)], fill=(0, 150, 255, 255), width=20)
        draw.line([(206, 50), (50, 206)], fill=(0, 150, 255, 255), width=20)
        
        # Save as ICO
        img.save('icon.ico', format='ICO')
        print("✓ Simple fallback icon created: icon.ico")
        
    except Exception as e2:
        print(f"Failed to create fallback icon: {e2}")
        print("Please create an icon.ico file manually or download one.")
