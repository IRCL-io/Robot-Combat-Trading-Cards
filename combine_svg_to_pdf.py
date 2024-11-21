import os
import cairosvg
from PyPDF2 import PdfMerger

def convert_svgs_to_pdf(svg_files, output_pdf):
    """Convert multiple SVG files to a single PDF."""
    pdf_files = []

    # Convert each SVG to a temporary PDF file
    for svg_file in svg_files:
        pdf_file = svg_file.replace(".svg", ".pdf")
        cairosvg.svg2pdf(url=svg_file, write_to=pdf_file)
        pdf_files.append(pdf_file)

    # Merge all temporary PDF files into one
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_pdf)
    merger.close()

    # Clean up temporary PDF files
    for pdf in pdf_files:
        os.remove(pdf)

    print(f"Combined PDF created: {output_pdf}")

# Example usage
svg_files = [
    "Antmageddon_robot_page_1.svg",
    "Antmageddon_robot_page_2.svg",
    "Antmageddon_robot_page_3.svg",
    "Antmageddon_robot_page_4.svg",
    "Antmageddon_robot_page_5.svg",
    "Antmageddon_robot_page_6.svg",
    "Antmageddon_card_back_page.svg"
]
output_pdf = "Antmageddon_combined.pdf"
convert_svgs_to_pdf(svg_files, output_pdf)
