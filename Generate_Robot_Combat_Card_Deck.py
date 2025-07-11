import json
import subprocess
import os
import glob

file_named = "Unspecified json"
event_named = "Unspecified Event"

# Page size: U.S. Letter at 300 dpi
PAGE_WIDTH = 2550
PAGE_HEIGHT = 3300

# Card layout: 3x3 grid with 1/8" (38 px) spacing
CARD_SPACING = 38  # 1/8 inch at 300 dpi = 37.5

CARD_WIDTH = 770 #824 originally.  Removed 54.
# pw 2550
# - 2310(cw 770 * 3) = 240
# - 76(cs 38 * 2) = 164
# / 2 = 82

LEFT_SIDE_OF_PAGE = 82 #previously 63
CARD_HEIGHT = 1074

GREY_COLOR = "rgb(210, 210, 210)"
DARKER_GREY_COLOR = "rgb(95, 95, 95)"
BACKGROUND_IMG_SIZE = 90  
NAME_FONT_SIZE = 84        
CORNER_SIZE = 40

from pypdf import PdfWriter, PdfReader

def assemble_pngs_to_pdf_with_alternating_backs(front_pngs, back_png, output_pdf):
    """Assemble PNGs into a PDF with alternating card back pages."""
    import img2pdf

    # Convert front PNGs to individual PDFs
    front_pdfs = []
    for front_png in front_pngs:
        front_pdf = front_png.replace('.png', '.pdf')
        with open(front_pdf, 'wb') as f:
            f.write(img2pdf.convert(front_png))
        front_pdfs.append(front_pdf)

    # Convert card back PNG to a PDF
    back_pdf = back_png.replace('.png', '.pdf')
    with open(back_pdf, 'wb') as f:
        f.write(img2pdf.convert(back_png))

    # Assemble the final PDF
    writer = PdfWriter()
    for front_pdf in front_pdfs:
        writer.append(PdfReader(front_pdf))
        writer.append(PdfReader(back_pdf))

    with open(output_pdf, 'wb') as f:
        writer.write(f)

    print(f"Generated PDF with alternating card backs: {output_pdf}")

    # Clean up intermediate PDFs
    for pdf in front_pdfs + [back_pdf]:
        os.remove(pdf)


def name_band(name):    
    name_font_size = NAME_FONT_SIZE if len(name) <= 13 else int(NAME_FONT_SIZE * 0.6)
    name_font_y = 116 if len(name) <= 13 else 104

    return f"""
        <rect x="40" y="40" width="{CARD_WIDTH - 80}" height="100" fill="{DARKER_GREY_COLOR}" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />

        <text x="{CARD_WIDTH / 2}" y="{name_font_y}" font-size="{name_font_size}" fill="black" text-anchor="middle" font-family="Roboto">{name}</text>
        <text x="{(CARD_WIDTH / 2) + 2}" y="{name_font_y + 2}" font-size="{name_font_size}" fill="white" text-anchor="middle" font-family="Roboto">{name}</text>
    """

def create_card_front(robot, x, y):
    """Generate an SVG snippet for an individual robot card at position (x, y)."""
    name = robot['name']
    weight = robot['weight']
    team = robot['team']
    image_url = robot['image_url']
    
    return f"""
    <g transform="translate({x}, {y})">
           <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="{GREY_COLOR}" stroke="black" rx="45" ry="45"/>
        <rect x="0" y="0" width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="url(#imagePattern)" /> 
        <image href="{image_url}" x="1" y="80" width="{CARD_WIDTH - 2}" height="{CARD_WIDTH - 2}"/>
        
        {name_band(name)}
        
        <rect x="40" y="{CARD_HEIGHT - 120}" width="{CARD_WIDTH - 80}" height="80" fill="{DARKER_GREY_COLOR}" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />

        <rect x="40" y="{CARD_HEIGHT - 254}" width="{CARD_WIDTH - 80}" height="120" fill="{DARKER_GREY_COLOR}" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />

        
        
        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 200}" font-size="36" fill="white" text-anchor="middle" font-family="Roboto">{weight}</text>  

        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 160}" font-size="36" fill="white" text-anchor="middle" font-family="Roboto">by {team}</text>
             
        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 65}" font-size="36" fill="white" text-anchor="middle" font-family="Roboto">{event_named}</text>

        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" stroke="black" stroke-width="10" fill="none" rx="45" ry="45" />   
    </g>
    """

def create_page_front(robots, page_num):
    svg_content = f"""
    <svg width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
        <style>
            @font-face {{
                font-family: 'Roboto';
                font-style: normal;
                font-weight: 400;
                src: url('https://fonts.gstatic.com/s/roboto/v29/KFOmCnqEu92Fr1Mu4mxP.ttf') format('truetype');
            }}
            @font-face {{
                font-family: 'Roboto';
                font-style: normal;
                font-weight: 700;
                src: url('https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfBBc9.ttf') format('truetype');
            }}
            text {{
                font-family: 'Roboto', sans-serif;
            }}
        </style>
        <defs>
            <pattern id="imagePattern" patternUnits="userSpaceOnUse" width="{BACKGROUND_IMG_SIZE}" height="{BACKGROUND_IMG_SIZE}">
                <image href="https://ircl-io.github.io/images/IRCL_logo_Transparent2.png" x="0" y="0" width="{BACKGROUND_IMG_SIZE}" height="{BACKGROUND_IMG_SIZE}" />
            </pattern>
        </defs>
        <rect x="0" y="0" width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}" fill="black" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />
    """

    cards_per_row = 3
    cards_per_column = 3
    max_cards_per_page = cards_per_row * cards_per_column

    print(f"Page {page_num}: {max_cards_per_page} cards maximum")
    print(f"Card layout: {cards_per_row}x{cards_per_column}, Card: {CARD_WIDTH}x{CARD_HEIGHT}, Spacing: {CARD_SPACING}px")

    robots_to_display = robots[:max_cards_per_page]

    for i, robot in enumerate(robots_to_display):
        row = i // cards_per_row
        col = i % cards_per_row
        x = col * (CARD_WIDTH + CARD_SPACING) + LEFT_SIDE_OF_PAGE
        y = row * (CARD_HEIGHT + CARD_SPACING) + 3
        print(f"Placing robot {i} at ({x}, {y})")
        svg_content += create_card_front(robot, x, y)

    svg_content += "</svg>"
    return svg_content

def create_card_back(x, y):
    """Generate an SVG snippet for a single card back positioned at (x, y)."""
    logo_image_url = "https://ircl-io.github.io/images/IRCL/IRCL_logo_Transparent-90.png"

    return f"""
    <g transform="translate({x}, {y})">
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="{GREY_COLOR}" stroke="black" rx="45" ry="45"/>
        <image href="{logo_image_url}" x="1" y="1" width="{CARD_WIDTH -2}" height="{CARD_HEIGHT-2}" stroke="black"  />
        <text x="60" y="60" font-size="64" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto" transform="rotate(90, 60, 120)">
            ircl.io
        </text>
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" stroke="black" stroke-width="10" fill="none" rx="45" ry="45" />  
    </g>
    """

def create_page_back():
    svg_content = f"""
    <svg width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
        <style>
            @font-face {{
                font-family: 'Roboto';
                font-style: normal;
                font-weight: 400;
                src: url('https://fonts.gstatic.com/s/roboto/v29/KFOmCnqEu92Fr1Mu4mxP.ttf') format('truetype');
            }}
            @font-face {{
                font-family: 'Roboto';
                font-style: normal;
                font-weight: 700;
                src: url('https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfBBc9.ttf') format('truetype');
            }}
            text {{
                font-family: 'Roboto', sans-serif;
            }}
        </style>
        <rect x="0" y="0" width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}" fill="black" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />
    """

    for row in range(3):
        for col in range(3):
            x = col * (CARD_WIDTH + CARD_SPACING) + LEFT_SIDE_OF_PAGE
            y = row * (CARD_HEIGHT + CARD_SPACING) + 3
            svg_content += create_card_back(x, y)

    svg_content += "</svg>"
    return svg_content

def svg_to_png_with_inkscape(svg_file, png_file):
    """Convert an SVG file to a PNG using Inkscape."""
    try:
        subprocess.run(["inkscape", svg_file, "--export-filename", png_file], check=True)
        print(f"Converted {svg_file} to {png_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion of {svg_file} to PNG: {e}")

def generate_robot_pages_with_png(json_file):
    """Generate paginated SVGs and convert them to PNGs."""
    with open(f"{json_file}.json", 'r') as f:
        data = json.load(f)
        robots = data.get("robots", [])

    max_cards_per_page = 9  # 3x3
    page_num = 1
    png_files = []

    for start in range(0, len(robots), max_cards_per_page):
        page_robots = robots[start:start + max_cards_per_page]
        if not page_robots:
            break
        svg_file = f"{json_file}_robot_page_{page_num}.svg"
        png_file = f"{json_file}_robot_page_{page_num}.png"

        page_svg = create_page_front(page_robots, page_num)
        with open(svg_file, 'w') as f:
            f.write(page_svg)

        print(f"Generated SVG for page {page_num}: {svg_file}")
        svg_to_png_with_inkscape(svg_file, png_file)
        png_files.append(png_file)
        os.remove(svg_file)

        page_num += 1

    # Create card back page
    card_back_svg = create_page_back()
    card_back_svg_file = f"{json_file}_card_back_page.svg"
    card_back_png_file = f"{json_file}_card_back_page.png"
    with open(card_back_svg_file, 'w') as f:
        f.write(card_back_svg)

    print(f"Generated SVG for card backs: {card_back_svg_file}")
    svg_to_png_with_inkscape(card_back_svg_file, card_back_png_file)
    png_files.append(card_back_png_file)
    os.remove(card_back_svg_file)

    print(f"All PNG files created: {png_files}")
    output_pdf = f"{json_file}_deck.pdf"
    assemble_pngs_to_pdf_with_alternating_backs(png_files[:-1], png_files[-1], output_pdf)
    print(f"Final PDF created: {output_pdf}")

def use_params(fil, eve):
    global file_named
    global event_named
    file_named = fil
    event_named = eve
    generate_robot_pages_with_png(file_named)
    for file_path in glob.glob('*.png'):
        os.remove(file_path)
    print(f"extra files removed")

# Start Here:
use_params("Bot Oblivion 2025", "Bot Oblivion 2025")
