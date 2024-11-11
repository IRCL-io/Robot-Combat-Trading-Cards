import json
import requests
import base64

def fetch_image_as_base64(url):
    """Fetch image from URL and convert to base64 to embed in SVG."""
    response = requests.get(url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    return None

def create_robot_card(robot, output_file):
    """Generate an SVG playing card for the robot."""
    name = robot['name']
    team = robot['team']
    image_base64 = fetch_image_as_base64(robot['image_url'])

    if image_base64 is None:
        print(f"Failed to retrieve image for {name}")
        return

    svg_content = f"""
    <svg width="300" height="450" xmlns="http://www.w3.org/2000/svg">
        <!-- Card Background -->
        <rect width="100%" height="100%" fill="lightgray" stroke="black" rx="15" ry="15"/>

        <!-- Robot Name -->
        <text x="50%" y="40" font-size="24" font-weight="bold" fill="black" text-anchor="middle">{name}</text>

        <!-- Robot Image -->
        <image href="data:image/png;base64,{image_base64}" x="50" y="60" width="200" height="200"/>

        <!-- Team Name -->
        <text x="50%" y="320" font-size="20" fill="darkblue" text-anchor="middle">Team: {team}</text>
    </svg>
    """

    with open(output_file, 'w') as f:
        f.write(svg_content)

def generate_robot_cards(json_file):
    """Read JSON data and generate SVG cards for each robot."""
    with open(json_file, 'r') as f:
        data = json.load(f)
        robots = data.get("antweight_robots", [])

    for robot in robots:
        output_file = f"{robot['name']}.svg"
        create_robot_card(robot, output_file)
        print(f"Generated {output_file}")

# Run the function with a specified JSON file
generate_robot_cards("Antmageddon.json")
