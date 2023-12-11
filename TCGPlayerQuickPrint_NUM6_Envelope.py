import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def get_most_recent_tcgplayer_csv(directory):
    """Fetch the most recent TCGPlayer CSV file from a given directory."""
    
    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Filter out files that don't match the TCGPlayer CSV naming pattern
    tcgplayer_files = [f for f in files if f.startswith('_TCGplayer_') and f.endswith('.csv')]

    if not tcgplayer_files:
        return None

    # Sort the files by last modified date
    sorted_files = sorted(tcgplayer_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

    # Return the most recently modified file
    return os.path.join(directory, sorted_files[0])


def create_pdf_from_csv(csv_path, output_path):
    """Generate a PDF with one address per page for #6 envelopes, centered in landscape orientation."""
    
    # Read the CSV data into a DataFrame
    df = pd.read_csv(csv_path)

    # Envelope dimensions for landscape orientation
    env_width = 6.5 * inch  # 6 1/2 inches (width)
    env_height = 3.625 * inch  # 3 5/8 inches (height)

    # Initialize the canvas (PDF) with the size of a #6 envelope in landscape
    c = canvas.Canvas(output_path, pagesize=(env_width, env_height))

    # Set font for text
    font_size = 12
    line_height = 14  # Adjust the line height as needed

    # Process each address and draw it on a new page
    for idx, row in df.iterrows():
        address = format_address_from_row(row)

        # Calculate the total height of the text block
        text_block_height = len(address) * line_height

        # Calculate the y position to start the address so it's centered
        y_position = (env_height + text_block_height) / 2

        for line in address:
            # Center each line of the address horizontally
            text_width = c.stringWidth(line, 'Helvetica', font_size)
            x_position = (env_width - text_width) / 2

            c.drawString(x_position, y_position, line)
            y_position -= line_height  # Move down for the next line

        # Create a new page for the next address
        if idx < len(df) - 1:
            c.showPage()

    c.save()

def format_address_from_row(row):
    """Format an address from a DataFrame row into a list of lines."""
    address = [f"{row['FirstName']} {row['LastName']}", row['Address1']]
    if pd.notna(row['Address2']) and row['Address2']:
        address.append(row['Address2'])
    address.append(f"{row['City']}, {row['State']} {row['PostalCode']}")
    return address

# Paths and function calls
downloads_folder = os.path.expanduser('~/Downloads')
csv_path = get_most_recent_tcgplayer_csv(downloads_folder)

if csv_path:
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_directory, 'addresses.pdf')
    create_pdf_from_csv(csv_path, output_path)
else:
    print("No matching CSV found.")
