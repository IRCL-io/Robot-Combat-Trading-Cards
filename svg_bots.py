import json
import subprocess
import os

file_named = "Unspecified json"
event_named = "Unspecified Parameter"

# Constants for page layout
PAGE_WIDTH = 816
PAGE_HEIGHT = 1056
CARD_WIDTH = 300
CARD_HEIGHT = 450
CARD_SPACING = 20
GREY_COLOR = "rgb(66, 66, 66)"

def svg_to_pdf_with_inkscape(svg_file, pdf_file):
    """Convert an SVG file to a PDF using Inkscape."""
    try:
        # Execute Inkscape command
        subprocess.run(
            ["inkscape", svg_file, "--export-filename", pdf_file],
            check=True
        )
        print(f"Converted {svg_file} to {pdf_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion of {svg_file} to PDF: {e}")

def create_robot_card_svg(robot, x, y):
    """Generate an SVG snippet for an individual robot card at position (x, y)."""
    name = robot['name']
    rank = robot['rank']
    weight = robot['weight']
    team = robot['team']
    image_url = robot['image_url']
    # Adjust font size for name based on character length
    name_font_size = 16 if len(name) > 24 else 24

    return f"""
    <g transform="translate({x}, {y})">
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="{GREY_COLOR}" stroke="black" rx="15" ry="15"/>
        
        <!-- Draw the rectangle using the pattern -->
        <rect x="0" y="0" width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="url(#imagePattern)" /> 

        <rect x="7" y="15" width="291" height="40" fill="{GREY_COLOR}" />
        <text x="{CARD_WIDTH / 2}" y="42" font-size="{name_font_size}"  fill="white" text-anchor="middle" font-family="Roboto">{name}</text>

        <image href="{image_url}" x="35" y="60" width="230" height="230"/>

        <rect x="35" y="308" width="230" height="120" fill="{GREY_COLOR}" />
        <text x="{CARD_WIDTH / 2}" y="330" font-size="20" fill="white" text-anchor="middle" font-family="Roboto">{rank}</text>
        <text x="{CARD_WIDTH / 2}" y="340" font-size="10" fill="white" text-anchor="middle" font-family="Roboto">{weight} weight</text>
        <text x="{CARD_WIDTH / 2}" y="360" font-size="10" fill="white" text-anchor="middle" font-family="Roboto">team</text>        
        <text x="{CARD_WIDTH / 2}" y="380" font-size="20" fill="white" text-anchor="middle" font-family="Roboto">{team}</text>
        <text x="{CARD_WIDTH / 2}" y="420" font-size="16" fill="white" text-anchor="middle" font-family="Roboto">{event_named}</text>
    </g>
    """

def create_page_svg(robots, page_num):
    """Generate a complete SVG page with a grid of robot cards."""
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
        <!-- Define the pattern -->
        <defs>
            <pattern id="imagePattern" patternUnits="userSpaceOnUse" width="50" height="50">
            <image href="https://ircl-io.github.io/images/IRCL_logo_Transparent2.png" x="0" y="0" width="50" height="50" />
            </pattern>
        </defs>
    """

    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT - 50) // (CARD_HEIGHT + CARD_SPACING)
    # max_cards_per_page = cards_per_row * cards_per_column

    for i, robot in enumerate(robots):
        row = i // cards_per_row
        col = i % cards_per_row
        x = col * (CARD_WIDTH + CARD_SPACING)
        y = row * (CARD_HEIGHT + CARD_SPACING)

        svg_content += create_robot_card_svg(robot, x, y)

    svg_content += "</svg>"
    return svg_content

def create_card_back(x, y):
    """Generate an SVG snippet for a single card back positioned at (x, y)."""
    logo_image_url = "https://ircl-io.github.io/images/IRCL_logo_Transparent2.png"
    return f"""
    <g transform="translate({x}, {y})">
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="{GREY_COLOR}" stroke="black" rx="15" ry="15"/>

        <image href="{logo_image_url}" x="1" y="-5" width="{CARD_WIDTH}" height="{CARD_HEIGHT+10}" stroke="black" />

        <text x="115" y="120" font-size="60" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto">
            IDAHO
        </text>
        <text x="122" y="200" font-size="60" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto">
            ROBOT
        </text>
        <text x="149" y="280" font-size="60" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto">
            COMBAT
        </text>
        <text x="135" y="360" font-size="60" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto">
            LEAGUE
        </text>
        <text x="150" y="415" font-size="32" font-weight="bold" fill="blue" text-anchor="middle" font-family="Roboto">
            https://ircl.io/
        </text>
    </g>
    """
         # <rect x="15" y="15" width="3" height="420" fill="white" stroke="white" />

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
        (PAGE_WIDTH - CARD_WIDTH, 0),                     # Top-right
        (PAGE_WIDTH - CARD_WIDTH, CARD_HEIGHT + CARD_SPACING),  # Below first card
        (PAGE_WIDTH - (2 * CARD_WIDTH) - CARD_SPACING, 0),              # Left of first card
        (PAGE_WIDTH - (2 * CARD_WIDTH) - CARD_SPACING, CARD_HEIGHT + CARD_SPACING)  # Below third card
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

    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT - 50) // (CARD_HEIGHT + CARD_SPACING)
    max_cards_per_page = cards_per_row * cards_per_column

    page_num = 1
    png_files = []
    for start in range(0, len(robots), max_cards_per_page):
        page_robots = robots[start:start + max_cards_per_page]
        svg_file = f"{json_file}_robot_page_{page_num}.svg"
        png_file = f"{json_file}_robot_page_{page_num}.png"

        # Generate SVG file
        page_svg = create_page_svg(page_robots, page_num)
        with open(svg_file, 'w') as f:
            f.write(page_svg)

        print(f"Generated {svg_file}")

        # Convert SVG to PNG
        svg_to_png_with_inkscape(svg_file, png_file)
        png_files.append(png_file)

        # Optionally delete the SVG if not needed
        # up to this point, the svg is the most efficient media,
        # but there are multiple advanced svg features with web 
        # # references which are resolved in the conversion to png
        os.remove(svg_file)

        page_num += 1

    # Generate and convert the card back page
    card_back_svg = create_card_back_page()
    card_back_svg_file = f"{json_file}_card_back_page.svg"
    card_back_png_file = f"{json_file}_card_back_page.png"

    with open(card_back_svg_file, 'w') as f:
        f.write(card_back_svg)

    print(f"Generated {card_back_svg_file}")

    svg_to_png_with_inkscape(card_back_svg_file, card_back_png_file)
    png_files.append(card_back_png_file)

    # Optionally delete the SVG if not needed
    # up to this point, the svg is the most efficient media,
    # but there are multiple advanced svg features with web 
    # # references which are resolved in the conversion to png
    os.remove(card_back_svg_file)

    print(f"All PNG files created: {png_files}")

def use_params(fil, eve):
    global file_named
    
    global event_named
    file_named = fil
    event_named = eve
    generate_robot_pages_with_png(file_named)

# and go
use_params("Antmageddon", "IRCL! Antmageddon 2024")