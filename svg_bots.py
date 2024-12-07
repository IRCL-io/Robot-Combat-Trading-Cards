import json
import subprocess
import os

file_named = "Unspecified json"
event_named = "Unspecified Parameter"

# Constants for page layout
PAGE_WIDTH = 2400 #778 #816 768 > width="2400" height="3150"
PAGE_HEIGHT = 3150 #1018 #1056 1008
CARD_WIDTH = 240
CARD_HEIGHT = 328
CARD_SPACING = 12
GREY_COLOR = "rgb(99, 99, 99)"
BACKGROUND_IMG_SIZE = 24
NAME_FONT_SIZE = 20

from PyPDF2 import PdfWriter, PdfReader

def assemble_pngs_to_pdf_with_alternating_backs(front_pngs, back_png, output_pdf):
    """Assemble PNGs into a PDF with alternating card back pages."""
    import img2pdf  # Install using `pip install img2pdf`

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

    # Assemble the final PDF with alternating pages
    writer = PdfWriter()
    for front_pdf in front_pdfs:
        writer.append(PdfReader(front_pdf))  # Add the front page
        writer.append(PdfReader(back_pdf))  # Add the card back page

    # Write the final PDF
    with open(output_pdf, 'wb') as f:
        writer.write(f)

    print(f"Generated PDF with alternating card backs: {output_pdf}")

    # Optionally clean up intermediate PDFs
    for pdf in front_pdfs + [back_pdf]:
        os.remove(pdf)

def create_robot_card_svg(robot, x, y):
    """Generate an SVG snippet for an individual robot card at position (x, y)."""
    name = robot['name']
    rank = robot['rank']
    weight = robot['weight']
    team = robot['team']
    image_url = robot['image_url']
    # Adjust font size for name based on character length
    name_font_size = 16 if len(name) > 17 else NAME_FONT_SIZE

    return f"""
    <g transform="translate({x}, {y})">
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="{GREY_COLOR}" stroke="black" rx="15" ry="15"/>
        
        <rect x="0" y="0" width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="url(#imagePattern)" /> 

        <rect x="16" y="12" width="{CARD_WIDTH - 32}" height="28" fill="{GREY_COLOR}"  rx="15" ry="15" />
        <text x="{CARD_WIDTH / 2}" y="32" font-size="{name_font_size}"  fill="white" text-anchor="middle" font-family="Roboto">{name}</text>

        <rect x="35" y="{CARD_HEIGHT - 75}" width="{CARD_WIDTH - 90}" height="30" fill="{GREY_COLOR}"  rx="15" ry="15" />

        <image href="{image_url}" x="1" y="42" width="{CARD_WIDTH - 2}" height="{CARD_WIDTH - 2}"/>

        <rect x="35" y="{CARD_HEIGHT - 52}" width="{CARD_WIDTH - 70}" height="42" fill="{GREY_COLOR}"  rx="15" ry="15" />

        
        <text x="{(CARD_WIDTH / 2) + 1}" y="{CARD_HEIGHT - 60}" 
            font-size="20" fill="black" text-anchor="middle" font-family="Roboto">{rank}</text>
        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 61}" 
            font-size="20" fill="white" text-anchor="middle" font-family="Roboto">{rank}</text>

              
        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 45}" font-size="10" fill="white" text-anchor="middle" font-family="Roboto">{weight} weight</text>

        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 28}" font-size="18" fill="white" text-anchor="middle" font-family="Roboto">{team}</text>
        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 14}" font-size="12" fill="white" text-anchor="middle" font-family="Roboto">{event_named}</text>
    </g>
    """

def create_page_svg(robots, page_num):
    """Generate a complete SVG page with a grid of robot cards."""
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
         <!-- Define the pattern -->
        <defs>
            <pattern id="imagePattern" patternUnits="userSpaceOnUse" width="{BACKGROUND_IMG_SIZE}" height="{BACKGROUND_IMG_SIZE}">
            <image href="https://ircl-io.github.io/images/IRCL_logo_Transparent2.png" x="0" y="0" width="{BACKGROUND_IMG_SIZE}" height="{BACKGROUND_IMG_SIZE}" />
            </pattern>
        </defs>
    """

    # Correctly calculate the number of cards per row and column
    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT + CARD_SPACING) // (CARD_HEIGHT + CARD_SPACING)
    max_cards_per_page = cards_per_row * cards_per_column

    print(f"Page dimensions: {PAGE_WIDTH}x{PAGE_HEIGHT}")
    print(f"Card dimensions: {CARD_WIDTH}x{CARD_HEIGHT} with {CARD_SPACING} spacing")
    print(f"Cards per row: {cards_per_row}, Cards per column: {cards_per_column}")
    print(f"Max cards per page: {max_cards_per_page}")

    robots_to_display = robots[:max_cards_per_page]

    for i, robot in enumerate(robots_to_display):
        row = i // cards_per_row
        col = i % cards_per_row
        x = col * (CARD_WIDTH + CARD_SPACING)
        y = row * (CARD_HEIGHT + CARD_SPACING)

        print(f"Placing robot {i} at ({x}, {y})")  # Debug placement

        svg_content += create_robot_card_svg(robot, x, y)

    svg_content += "</svg>"
    return svg_content

def create_card_back(x, y):
    """Generate an SVG snippet for a single card back positioned at (x, y)."""
    logo_image_url = "https://ircl-io.github.io/images/IRCL/IRCL_logo_Transparent-90.png"

    return f"""
    <g transform="translate({x}, {y})">
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="{GREY_COLOR}" stroke="black" rx="15" ry="15"/>

        <image href="{logo_image_url}" x="1" y="1" width="{CARD_WIDTH -2}" height="{CARD_HEIGHT-2}" stroke="black"  />

        <text x="60" y="10" font-size="32" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto" transform="rotate(90, 10, 10)" >
            ircl.io
        </text>
    </g>
    """

def create_card_back_page():
    """Generate a page containing four card backs."""
    svg_content = f"""
    <svg width="{PAGE_WIDTH}" height="{PAGE_HEIGHT}" xmlns="http://www.w3.org/2000/svg">
        <!-- Link to Google Roboto font using @font-face -->
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
    """

    # Top-right aligned positions for four card backs
    positions = [
        (PAGE_WIDTH - CARD_WIDTH, 0), # Top-right
        (PAGE_WIDTH - CARD_WIDTH, CARD_HEIGHT + CARD_SPACING),
        (PAGE_WIDTH - CARD_WIDTH, (2 * CARD_HEIGHT) + (2 * CARD_SPACING)),
        (PAGE_WIDTH - (2 * CARD_WIDTH) - CARD_SPACING, 0),              
        (PAGE_WIDTH - (2 * CARD_WIDTH) - CARD_SPACING, CARD_HEIGHT + CARD_SPACING),   
        (PAGE_WIDTH - (2 * CARD_WIDTH) - CARD_SPACING, (2 * CARD_HEIGHT) + (2 * CARD_SPACING)),       
        (PAGE_WIDTH - (3 * CARD_WIDTH) - (2 * CARD_SPACING), 0),              
        (PAGE_WIDTH - (3 * CARD_WIDTH) - (2 * CARD_SPACING), CARD_HEIGHT + CARD_SPACING),  
        (PAGE_WIDTH - (3 * CARD_WIDTH) - (2 * CARD_SPACING), (2 * CARD_HEIGHT) + (2 * CARD_SPACING)) 
    ]

    for x, y in positions:
        svg_content += create_card_back(x, y)

    svg_content += "</svg>"
    return svg_content

def svg_to_png_with_inkscape(svg_file, png_file):
    """Convert an SVG file to a PNG using Inkscape."""
    try:
        # Execute Inkscape command to export as PNG
        subprocess.run(
            ["inkscape", svg_file, "--export-filename", png_file],
            check=True
        )
        print(f"Converted {svg_file} to {png_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion of {svg_file} to PNG: {e}")

def generate_robot_pages_with_png(json_file):
    """Generate paginated SVGs and convert them to PNGs."""
    with open(f"{json_file}.json", 'r') as f:
        data = json.load(f)
        robots = data.get("robots", [])

    # Calculate cards per row, column, and total per page
    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT + CARD_SPACING) // (CARD_HEIGHT + CARD_SPACING)
    max_cards_per_page = cards_per_row * cards_per_column

    print(f"Cards per row: {cards_per_row}, Cards per column: {cards_per_column}")
    print(f"Max cards per page: {max_cards_per_page}")
    print(f"Page dimensions: {PAGE_WIDTH}x{PAGE_HEIGHT}")
    print(f"Card dimensions: {CARD_WIDTH}x{CARD_HEIGHT} with {CARD_SPACING} spacing")

    page_num = 1  # Start page numbering from 1
    png_files = []

    # Loop through robots in chunks of `max_cards_per_page`
    for start in range(0, len(robots), max_cards_per_page):
        # Slice robots for the current page
        page_robots = robots[start:start + max_cards_per_page]

        # Define filenames for the SVG and PNG
        svg_file = f"{json_file}_robot_page_{page_num}.svg"
        png_file = f"{json_file}_robot_page_{page_num}.png"

        # Generate SVG content
        page_svg = create_page_svg(page_robots, page_num)

        # Write the SVG file
        with open(svg_file, 'w') as f:
            f.write(page_svg)

        print(f"Generated SVG for page {page_num}: {svg_file}")

        # Convert SVG to PNG using Inkscape
        svg_to_png_with_inkscape(svg_file, png_file)
        png_files.append(png_file)

        # Optionally delete the SVG file
        os.remove(svg_file)

        # Increment page number
        page_num += 1

    # Generate and convert the card back page
    card_back_svg = create_card_back_page()
    card_back_svg_file = f"{json_file}_card_back_page.svg"
    card_back_png_file = f"{json_file}_card_back_page.png"

    with open(card_back_svg_file, 'w') as f:
        f.write(card_back_svg)

    print(f"Generated SVG for card backs: {card_back_svg_file}")

    svg_to_png_with_inkscape(card_back_svg_file, card_back_png_file)
    png_files.append(card_back_png_file)

    # Optionally delete the SVG file for card backs
    os.remove(card_back_svg_file)

    print(" ")
    print(f"All PNG files created: {png_files}")
    print(" ")
    # After all PNGs are created:
    output_pdf = f"{json_file}_cards_with_backs.pdf"
    assemble_pngs_to_pdf_with_alternating_backs(png_files[:-1], png_files[-1], output_pdf)
    print(f"Final PDF created: {output_pdf}")

def use_params(fil, eve):
    global file_named
    
    global event_named
    file_named = fil
    event_named = eve
    generate_robot_pages_with_png(file_named)

# and go
use_params("Antmageddon", "IRCL! Antmageddon 2024")