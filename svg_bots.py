import json

file_named = "Unspecified json"
event_named = "Unspecified Parameter"

# Constants for page layout
PAGE_WIDTH = 816
PAGE_HEIGHT = 1056
CARD_WIDTH = 300
CARD_HEIGHT = 450
CARD_SPACING = 20

def create_robot_card_svg(robot, x, y):
    """Generate an SVG snippet for an individual robot card at position (x, y)."""
    name = robot['name']
    rank = robot['rank']
    weight = robot['weight']
    team = robot['team']
    image_url = robot['image_url']
    logo_image_url = "https://ircl-io.github.io/images/IRCL_logo_Transparent2.png"

    return f"""
    <g transform="translate({x}, {y})">
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="rgb(51, 51, 51)" stroke="black" rx="15" ry="15"/>
        <image href="{logo_image_url}" x="1" y="14" width="290" stroke="black" />
        <text x="{CARD_WIDTH / 2}" y="42" font-size="24" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto">{name}</text>
        <image href="{image_url}" x="35" y="60" width="230" height="230"/>
        <text x="{CARD_WIDTH / 2}" y="330" font-size="20" fill="white" text-anchor="middle" font-family="Roboto">{rank}</text>

        <text x="{CARD_WIDTH / 2}" y="340" font-size="10" fill="white" text-anchor="middle" font-family="Roboto">{weight} weight</text>
        <text x="{CARD_WIDTH / 2}" y="360" font-size="10" fill="white" text-anchor="middle" font-family="Roboto">team</text>

        <rect x="0" y="353" width="300" height="40" fill="rgba(51, 51, 51, 0.5)" />
        <text x="{CARD_WIDTH / 2}" y="380" font-size="20" fill="white" text-anchor="middle" font-family="Roboto">{team}</text>
        <text x="{CARD_WIDTH / 2}" y="420" font-size="16" fill="grey" text-anchor="middle" font-family="Roboto">{event_named}</text>
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

        
    """
# <text x="30%" y="30" font-size="24" font-weight="bold" text-anchor="middle">{event_named} ~ Page {page_num}</text>
    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT - 50) // (CARD_HEIGHT + CARD_SPACING)
    max_cards_per_page = cards_per_row * cards_per_column

    for i, robot in enumerate(robots):
        row = i // cards_per_row
        col = i % cards_per_row
        x = col * (CARD_WIDTH + CARD_SPACING)
        y = row * (CARD_HEIGHT + CARD_SPACING)

        svg_content += create_robot_card_svg(robot, x, y)

    svg_content += "</svg>"
    return svg_content

def generate_robot_pages(json_file):
    """Read JSON data and generate paginated SVG pages for robot cards."""
    with open(f"{json_file}.json", 'r') as f:
        data = json.load(f)
        robots = data.get("robots", [])

    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT - 50) // (CARD_HEIGHT + CARD_SPACING)
    max_cards_per_page = cards_per_row * cards_per_column

    page_num = 1
    for start in range(0, len(robots), max_cards_per_page):
        page_robots = robots[start:start + max_cards_per_page]
        page_svg = create_page_svg(page_robots, page_num)
        
        output_file = f"{json_file}_robot_page_{page_num}.svg"
        with open(output_file, 'w') as f:
            f.write(page_svg)
        
        print(f"Generated {output_file}")
        page_num += 1

def use_params(fil, eve):
    global file_named
    
    global event_named
    file_named = fil
    event_named = eve
    generate_robot_pages(file_named)

# and go
use_params("Antmageddon", "IRCL! Antmageddon 2024")