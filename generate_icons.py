import math
from PIL import Image, ImageDraw, ImageFilter

def draw_suv_icon(size):
    # Base canvas
    img = Image.new('RGBA', (size, size), (2, 2, 5, 255)) # match #020205 background
    draw = ImageDraw.Draw(img)
    
    # Scale coordinates based on size
    scale = size / 512.0
    center = size / 2
    
    # Draw dark glowing background ring
    r_outer = 230 * scale
    draw.ellipse(
        [center - r_outer, center - r_outer, center + r_outer, center + r_outer],
        fill=(13, 10, 8, 255),
        outline=(217, 160, 74, 255), # #d9a04a
        width=int(10 * scale)
    )

    # Add a soft amber glow to the ring using a second blurred image
    glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.ellipse(
        [center - r_outer, center - r_outer, center + r_outer, center + r_outer],
        outline=(217, 160, 74, 120),
        width=int(25 * scale)
    )
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(10 * scale))
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img) # Re-bind draw

    # --- Draw Stylized SUV Front Profile (Apocalypse Survival style) ---
    
    # 1. Main cabin trapezoid (Windshield area)
    # y range: 150 to 220
    draw.polygon([
        ((center - 110) * scale, 150 * scale),
        ((center + 110) * scale, 150 * scale),
        ((center + 160) * scale, 220 * scale),
        ((center - 160) * scale, 220 * scale)
    ], fill=(30, 30, 40, 255), outline=(217, 160, 74, 255), width=int(3 * scale))
    
    # Windshield glass (inner)
    draw.polygon([
        ((center - 100) * scale, 160 * scale),
        ((center + 100) * scale, 160 * scale),
        ((center + 145) * scale, 210 * scale),
        ((center - 145) * scale, 210 * scale)
    ], fill=(15, 23, 42, 255))

    # 2. Main lower body (Hood/Grille area)
    # y range: 220 to 360
    draw.rectangle([
        (center - 200) * scale, 220 * scale,
        (center + 200) * scale, 360 * scale
    ], fill=(20, 20, 25, 255), outline=(217, 160, 74, 255), width=int(5 * scale))

    # 3. Off-road tires at the bottom (sides)
    # y range: 250 to 360
    # Left tire
    draw.rectangle([
        (center - 220) * scale, 250 * scale,
        (center - 170) * scale, 360 * scale
    ], fill=(10, 10, 12, 255), outline=(217, 160, 74, 180), width=int(3 * scale))
    # Right tire
    draw.rectangle([
        (center + 170) * scale, 250 * scale,
        (center + 220) * scale, 360 * scale
    ], fill=(10, 10, 12, 255), outline=(217, 160, 74, 180), width=int(3 * scale))

    # Treads on tires (simple horizontal lines)
    for y_tr in range(int(260 * scale), int(355 * scale), int(15 * scale)):
        draw.line([((center - 220) * scale, y_tr), ((center - 170) * scale, y_tr)], fill=(217, 160, 74, 100), width=int(2 * scale))
        draw.line([((center + 170) * scale, y_tr), ((center + 220) * scale, y_tr)], fill=(217, 160, 74, 100), width=int(2 * scale))

    # 4. Rugged Grille
    # y range: 230 to 290
    draw.rectangle([
        (center - 120) * scale, 230 * scale,
        (center + 120) * scale, 290 * scale
    ], fill=(12, 12, 16, 255), outline=(217, 160, 74, 200), width=int(3 * scale))
    
    # Grille vertical slots
    for i in range(-4, 5, 2):
        dx = i * 22 * scale
        draw.rectangle([
            center + dx - 5 * scale, 238 * scale,
            center + dx + 5 * scale, 282 * scale
        ], fill=(217, 160, 74, 255))

    # 5. Glowing Headlights (survival high-beams)
    # y = 250
    hl_size = 36 * scale
    hl_y = 250 * scale
    hl_lx = (center - 160) * scale
    hl_rx = (center + 160) * scale
    
    # Left Headlight
    draw.ellipse([hl_lx - hl_size/2, hl_y - hl_size/2, hl_lx + hl_size/2, hl_y + hl_size/2], fill=(255, 220, 150, 255), outline=(217, 160, 74, 255), width=int(3 * scale))
    # Right Headlight
    draw.ellipse([hl_rx - hl_size/2, hl_y - hl_size/2, hl_rx + hl_size/2, hl_y + hl_size/2], fill=(255, 220, 150, 255), outline=(217, 160, 74, 255), width=int(3 * scale))

    # Add light beams/flare effect on a separate layer
    beams = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    beams_draw = ImageDraw.Draw(beams)
    
    # Outer bright yellow flare
    beams_draw.ellipse([hl_lx - hl_size, hl_y - hl_size, hl_lx + hl_size, hl_y + hl_size], fill=(255, 217, 120, 80))
    beams_draw.ellipse([hl_rx - hl_size, hl_y - hl_size, hl_rx + hl_size, hl_y + hl_size], fill=(255, 217, 120, 80))
    
    # Scale/blur light flares
    beams = beams.filter(ImageFilter.GaussianBlur(8 * scale))
    img = Image.alpha_composite(img, beams)
    draw = ImageDraw.Draw(img) # Re-bind draw

    # 6. Roof Rack with spot lights
    # y = 145
    draw.line([((center - 130) * scale, 145 * scale), ((center + 130) * scale, 145 * scale)], fill=(217, 160, 74, 255), width=int(6 * scale))
    
    # Spot lights (4 lights on the rack)
    for i in [-3, -1, 1, 3]:
        sx = center + i * 32
        draw.rectangle([
            (sx - 10) * scale, 127 * scale,
            (sx + 10) * scale, 145 * scale
        ], fill=(25, 25, 30, 255), outline=(217, 160, 74, 255), width=int(2 * scale))
        draw.ellipse([
            (sx - 7) * scale, 130 * scale,
            (sx + 7) * scale, 142 * scale
        ], fill=(255, 230, 170, 255))

    # 7. Heavy Bumper & Winch
    # y range: 340 to 375
    draw.rectangle([
        (center - 215) * scale, 340 * scale,
        (center + 215) * scale, 375 * scale
    ], fill=(40, 40, 45, 255), outline=(217, 160, 74, 255), width=int(4 * scale))
    
    # Winch roller in the middle
    draw.rectangle([
        (center - 40) * scale, 348 * scale,
        (center + 40) * scale, 367 * scale
    ], fill=(15, 15, 18, 255), outline=(217, 160, 74, 180), width=int(2 * scale))
    
    # Steel cable wraps (horizontal stripes)
    for sx in range(int((center - 30) * scale), int((center + 35) * scale), int(8 * scale)):
        draw.line([(sx, 352 * scale), (sx, 363 * scale)], fill=(180, 180, 180, 255), width=int(3 * scale))

    # 8. Add stylized text "SUV" at the bottom inside the ring
    logo_y = 390
    draw.polygon([
        ((center - 110) * scale, logo_y * scale),
        ((center + 110) * scale, logo_y * scale),
        ((center + 90) * scale, (logo_y + 55) * scale),
        ((center - 90) * scale, (logo_y + 55) * scale)
    ], fill=(15, 15, 20, 255), outline=(217, 160, 74, 255), width=int(3 * scale))
    
    # Let's draw stylized block letters for S - U - V
    # S
    s_x = (center - 60) * scale
    s_y = (logo_y + 12) * scale
    draw.line([(s_x + 25*scale, s_y), (s_x, s_y), (s_x, s_y + 15*scale), (s_x + 25*scale, s_y + 15*scale), (s_x + 25*scale, s_y + 30*scale), (s_x, s_y + 30*scale)], fill=(217, 160, 74, 255), width=int(6*scale))
    
    # U
    u_x = (center - 12) * scale
    u_y = (logo_y + 12) * scale
    draw.line([(u_x, u_y), (u_x, u_y + 24*scale), (u_x + 24*scale, u_y + 24*scale), (u_x + 24*scale, u_y)], fill=(217, 160, 74, 255), width=int(6*scale))
    
    # V
    v_x = (center + 36) * scale
    v_y = (logo_y + 12) * scale
    draw.line([(v_x, v_y), (v_x + 12*scale, v_y + 30*scale), (v_x + 24*scale, v_y)], fill=(217, 160, 74, 255), width=int(6*scale))

    return img

# Generate both icons
icon_512 = draw_suv_icon(512)
icon_512.save('/root/Game/icon-512.png', 'PNG')

icon_192 = draw_suv_icon(192)
icon_192.save('/root/Game/icon-192.png', 'PNG')

print("PWA Icons generated successfully!")
