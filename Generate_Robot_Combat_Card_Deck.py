import argparse
import os
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter

# Page size: U.S. Letter at 300 dpi
PAGE_WIDTH = 2550
PAGE_HEIGHT = 3300

# Card layout: 3x3 grid with 1/8" (38 px) spacing
CARD_SPACING = 38  # 1/8 inch at 300 dpi = 37.5

CARD_WIDTH = 770  # 824 originally. Removed 54.
LEFT_SIDE_OF_PAGE = 82  # previously 63
CARD_HEIGHT = 1074

GREY_COLOR = "rgb(210, 210, 210)"
DARKER_GREY_COLOR = "rgb(95, 95, 95)"
BACKGROUND_IMG_SIZE = 90
NAME_FONT_SIZE = 84
CORNER_SIZE = 40


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", text.strip())
    slug = slug.strip("_")
    return slug or "event"


def assemble_pngs_to_pdf_with_alternating_backs(front_pngs, back_png, output_pdf: Path) -> None:
    """Assemble PNGs into a PDF with alternating card back pages."""
    import img2pdf

    front_pdfs = []
    for front_png in front_pngs:
        front_pdf = Path(str(front_png).replace(".png", ".pdf"))
        with open(front_pdf, "wb") as f:
            f.write(img2pdf.convert(str(front_png)))
        front_pdfs.append(front_pdf)

    back_pdf = Path(str(back_png).replace(".png", ".pdf"))
    with open(back_pdf, "wb") as f:
        f.write(img2pdf.convert(str(back_png)))

    writer = PdfWriter()
    for front_pdf in front_pdfs:
        writer.append(PdfReader(str(front_pdf)))
        writer.append(PdfReader(str(back_pdf)))

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Generated PDF with alternating card backs: {output_pdf}")

    for pdf in front_pdfs + [back_pdf]:
        pdf.unlink(missing_ok=True)


def name_band(name: str) -> str:
    name_font_size = NAME_FONT_SIZE if len(name) <= 13 else int(NAME_FONT_SIZE * 0.6)
    name_font_y = 116 if len(name) <= 13 else 104

    return f"""
        <rect x="40" y="40" width="{CARD_WIDTH - 80}" height="100" fill="{DARKER_GREY_COLOR}" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />

        <text x="{CARD_WIDTH / 2}" y="{name_font_y}" font-size="{name_font_size}" fill="black" text-anchor="middle" font-family="Roboto">{name}</text>
        <text x="{(CARD_WIDTH / 2) + 2}" y="{name_font_y + 2}" font-size="{name_font_size}" fill="white" text-anchor="middle" font-family="Roboto">{name}</text>
    """


def create_card_front(robot, x, y, event_name: str) -> str:
    """Generate an SVG snippet for an individual robot card at position (x, y)."""
    name = robot["name"]
    weight = robot["weight"]
    team = robot["team"]
    image_url = robot["image_url"]

    return f"""
    <g transform="translate({x}, {y})">
           <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="{GREY_COLOR}" stroke="black" rx="45" ry="45"/>
        <rect x="0" y="0" width="{CARD_WIDTH}" height="{CARD_HEIGHT}" fill="url(#imagePattern)" />
        <image href="{image_url}" x="1" y="80" width="{CARD_WIDTH - 2}" height="{CARD_WIDTH - 2}"/>

        {name_band(name)}

        <rect x="40" y="{CARD_HEIGHT - 120}" width="{CARD_WIDTH - 80}" height="80" fill="{DARKER_GREY_COLOR}" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />

        <rect x="40" y="{CARD_HEIGHT - 254}" width="{CARD_WIDTH - 80}" height="120" fill="{DARKER_GREY_COLOR}" rx="{CORNER_SIZE}" ry="{CORNER_SIZE}" />

        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 205}" font-size="36" fill="white" text-anchor="middle" font-family="Roboto">{weight}</text>
        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 165}" font-size="36" fill="white" text-anchor="middle" font-family="Roboto">by {team}</text>

        <text x="{CARD_WIDTH / 2}" y="{CARD_HEIGHT - 70}" font-size="36" fill="white" text-anchor="middle" font-family="Roboto">{event_name}</text>

        <rect width="{CARD_WIDTH}" height="{CARD_HEIGHT}" stroke="black" stroke-width="10" fill="none" rx="45" ry="45" />
    </g>
    """


def create_page_front(robots, page_num: int, event_name: str) -> str:
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
        svg_content += create_card_front(robot, x, y, event_name)

    svg_content += "</svg>"
    return svg_content


def create_card_back(x, y) -> str:
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


def create_page_back() -> str:
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


def svg_to_png_with_inkscape(svg_file: Path, png_file: Path) -> None:
    """Convert an SVG file to a PNG using Inkscape."""
    try:
        subprocess.run(
            ["inkscape", str(svg_file), "--export-filename", str(png_file)],
            check=True,
        )
        print(f"Converted {svg_file} to {png_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion of {svg_file} to PNG: {e}")


def parse_ttdb_sections(ttdb_text: str):
    sections = []
    for block in re.split(r"^\\s*---+\\s*$", ttdb_text, flags=re.M):
        lines = [line.rstrip("\\n") for line in block.splitlines()]
        header_line = None
        for line in lines:
            if line.startswith("@LAT"):
                header_line = line.strip()
                break
        if not header_line:
            continue
        record_id = header_line.split()[0]
        relates_match = re.search(r"relates:([^|]+)", header_line)
        relates_raw = relates_match.group(1).strip() if relates_match else ""
        relates = []
        if relates_raw:
            for token in relates_raw.split(","):
                token = token.strip()
                if not token:
                    continue
                if ">@" in token:
                    edge_type, target = token.split(">@", 1)
                    relates.append((edge_type.strip(), f"@{target.strip()}"))
                elif ">" in token:
                    edge_type, target = token.split(">", 1)
                    relates.append((edge_type.strip(), target.strip()))
        title = None
        for line in lines:
            if line.startswith("## "):
                title = line.replace("## ", "", 1).strip()
                break
        sections.append(
            {
                "record_id": record_id,
                "header": header_line,
                "title": title,
                "lines": lines,
                "relates": relates,
            }
        )
    return sections


def parse_event_block(section):
    event = {"name": None, "url": None, "location": None, "dates": None}
    if section.get("title"):
        event_title = section["title"].replace("(Event)", "").strip()
        event["name"] = event_title
    for line in section.get("lines", []):
        if line.strip().startswith("- URL:"):
            event["url"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("- Location:"):
            event["location"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("- Dates:"):
            event["dates"] = line.split(":", 1)[1].strip()
    return event


def parse_robot_block(section):
    robot = {"name": None, "weight": None, "team": None, "image_url": None}
    if section.get("title"):
        robot["name"] = section["title"].strip()
    for line in section.get("lines", []):
        stripped = line.strip()
        if stripped.startswith("- Weight class:"):
            robot["weight"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Team:"):
            robot["team"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("- Image:"):
            robot["image_url"] = stripped.split(":", 1)[1].strip()
    return robot


def load_event_from_ttdb(ttdb_path: Path, event_name: str):
    ttdb_text = ttdb_path.read_text(encoding="utf-8")
    sections = parse_ttdb_sections(ttdb_text)
    event_section = None
    for section in sections:
        title = section.get("title")
        if not title:
            continue
        normalized = title.replace("(Event)", "").strip()
        if normalized.lower() == event_name.lower():
            event_section = section
            break
    if not event_section:
        raise ValueError(f"Event not found in TTDB: {event_name}")

    event = parse_event_block(event_section)
    event_id = event_section["record_id"]

    robots = []
    for section in sections:
        if section["record_id"] == event_id:
            continue
        relates = section.get("relates", [])
        if not any(edge == "competes_in" and target == event_id for edge, target in relates):
            continue
        robot = parse_robot_block(section)
        if all(robot.values()):
            robots.append(robot)
        else:
            missing = [k for k, v in robot.items() if not v]
            print(f"Skipping robot {robot.get('name') or section['record_id']}: missing {missing}")

    if not robots:
        raise ValueError(f"No robots linked to event {event_name} via competes_in edges.")

    event_name_final = event.get("name") or event_name
    return event, robots, event_name_final


def generate_robot_pages_with_png(
    ttdb_path: Path,
    event_name: str,
    cards_dir: Path,
    output_dir: Path,
    keep_svgs: bool,
    keep_pngs: bool,
) -> Path:
    """Generate paginated SVGs and convert them to PNGs."""
    _event, robots, event_name = load_event_from_ttdb(ttdb_path, event_name)

    cards_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    svg_dir = cards_dir / "svgs"
    svg_dir.mkdir(parents=True, exist_ok=True)

    max_cards_per_page = 9  # 3x3
    page_num = 1
    png_files = []
    event_slug = slugify(event_name)

    for start in range(0, len(robots), max_cards_per_page):
        page_robots = robots[start : start + max_cards_per_page]
        if not page_robots:
            break
        svg_file = svg_dir / f"{event_slug}_robot_page_{page_num}.svg"
        png_file = cards_dir / f"{event_slug}_robot_page_{page_num}.png"

        page_svg = create_page_front(page_robots, page_num, event_name)
        svg_file.write_text(page_svg, encoding="utf-8")

        print(f"Generated SVG for page {page_num}: {svg_file}")
        svg_to_png_with_inkscape(svg_file, png_file)
        png_files.append(png_file)

        page_num += 1

    card_back_svg = create_page_back()
    card_back_svg_file = svg_dir / f"{event_slug}_card_back_page.svg"
    card_back_png_file = cards_dir / f"{event_slug}_card_back_page.png"
    card_back_svg_file.write_text(card_back_svg, encoding="utf-8")

    print(f"Generated SVG for card backs: {card_back_svg_file}")
    svg_to_png_with_inkscape(card_back_svg_file, card_back_png_file)
    png_files.append(card_back_png_file)

    print(f"All PNG files created: {png_files}")
    output_pdf = output_dir / f"{event_slug}_deck.pdf"
    assemble_pngs_to_pdf_with_alternating_backs(png_files[:-1], png_files[-1], output_pdf)
    print(f"Final PDF created: {output_pdf}")

    if not keep_svgs:
        for svg_path in svg_dir.glob("*.svg"):
            svg_path.unlink(missing_ok=True)
        try:
            svg_dir.rmdir()
        except OSError:
            pass

    if not keep_pngs:
        for png_path in png_files:
            png_path.unlink(missing_ok=True)

    return output_pdf


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate robot combat card decks.")
    parser.add_argument(
        "--ttdb",
        "-t",
        default="cards/IRCL_TTDB.md",
        help="Path to the IRCL TTDB markdown file.",
    )
    parser.add_argument(
        "--event-name",
        required=True,
        help="Event name to render (must match an Event title in the TTDB).",
    )
    parser.add_argument(
        "--cards-dir",
        default=None,
        help="Directory for generated card PNGs.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for generated PDFs.",
    )
    parser.add_argument(
        "--keep-svgs",
        action="store_true",
        help="Keep intermediate SVG pages.",
    )
    parser.add_argument(
        "--cleanup-pngs",
        action="store_true",
        help="Remove PNGs after PDF assembly.",
    )

    args = parser.parse_args()
    ttdb_path = Path(args.ttdb)
    if not ttdb_path.exists():
        raise FileNotFoundError(f"TTDB input not found: {ttdb_path}")

    event_name = args.event_name
    event_slug = slugify(event_name)

    base_dir = Path(__file__).resolve().parent
    cards_dir = Path(args.cards_dir) if args.cards_dir else base_dir / "cards" / event_slug
    output_dir = Path(args.output_dir) if args.output_dir else base_dir / "output" / event_slug

    print(f"Event: {event_name}")
    event, _robots, resolved_name = load_event_from_ttdb(ttdb_path, event_name)
    if resolved_name != event_name:
        print(f"Resolved event name: {resolved_name}")
    if event:
        print(f"Event source: {event.get('url', 'unknown')}")
    print(f"Cards dir: {cards_dir}")
    print(f"Output dir: {output_dir}")

    generate_robot_pages_with_png(
        ttdb_path=ttdb_path,
        event_name=event_name,
        cards_dir=cards_dir,
        output_dir=output_dir,
        keep_svgs=args.keep_svgs,
        keep_pngs=not args.cleanup_pngs,
    )


if __name__ == "__main__":
    main()
