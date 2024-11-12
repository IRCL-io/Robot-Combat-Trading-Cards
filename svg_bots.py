import json

file_named = "Antmageddon ants.json"
weight_class = "ant"
event_named = "IRCL Antmageddon 2024"

# Constants for page layout
PAGE_WIDTH = 816
PAGE_HEIGHT = 1056
CARD_WIDTH = 300
CARD_HEIGHT = 450
CARD_SPACING = 20

def create_robot_card_svg(robot, x, y):
    """Generate an SVG snippet for an individual robot card at position (x, y)."""
    name = robot['name']
    team = robot['team']
    image_url = robot['image_url']
    
    return f"""
    <g transform="translate({x}, {y})">
        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="charcoal" stroke="black" rx="15" ry="15"/>
        <text x="{CARD_WIDTH / 2}" y="40" font-size="24" font-weight="bold" fill="white" text-anchor="middle" font-family="Roboto">{name}</text>
        <image href="{image_url}" x="50" y="60" width="200" height="200"/>
        <text x="{CARD_WIDTH / 2}" y="320" font-size="20" fill="lightblue" text-anchor="middle" font-family="Roboto">{team}</text>
        <text x="{CARD_WIDTH / 2}" y="420" font-size="10" fill="grey" text-anchor="middle" font-family="Roboto">{event_named}</text>
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

        <text x="30%" y="30" font-size="24" font-weight="bold" text-anchor="middle">{event_named} ~ Page {page_num}</text>
    """

    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT - 50) // (CARD_HEIGHT + CARD_SPACING)
    max_cards_per_page = cards_per_row * cards_per_column

    for i, robot in enumerate(robots):
        row = i // cards_per_row
        col = i % cards_per_row
        x = col * (CARD_WIDTH + CARD_SPACING)
        y = row * (CARD_HEIGHT + CARD_SPACING) + 50

        svg_content += create_robot_card_svg(robot, x, y)

    svg_content += "</svg>"
    return svg_content


def generate_robot_pages(json_file):
    """Read JSON data and generate paginated SVG pages for robot cards."""
    with open(json_file, 'r') as f:
        data = json.load(f)
        robots = data.get("robots", [])

    cards_per_row = PAGE_WIDTH // (CARD_WIDTH + CARD_SPACING)
    cards_per_column = (PAGE_HEIGHT - 50) // (CARD_HEIGHT + CARD_SPACING)
    max_cards_per_page = cards_per_row * cards_per_column

    page_num = 1
    for start in range(0, len(robots), max_cards_per_page):
        page_robots = robots[start:start + max_cards_per_page]
        page_svg = create_page_svg(page_robots, page_num)
        
        output_file = f"{weight_class}_robot_page_{page_num}.svg"
        with open(output_file, 'w') as f:
            f.write(page_svg)
        
        print(f"Generated {output_file}")
        page_num += 1

def use_params(fil, wei, eve):
    global file_named
    global weight_class
    global event_named
    file_named = fil
    weight_class = wei
    event_named = eve
    generate_robot_pages(file_named)

# and go
# use_params("Antmageddon ants.json", "ant", "IRCL!! Antmageddon 2024")
