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
    """Generate a PDF with address labels from a given CSV path."""
    
    # Read the CSV data into a DataFrame
    print("Reading the CSV file...")
    df = pd.read_csv(csv_path)
    print(f"Found {len(df)} addresses.")

    # Initialize the canvas (PDF) with a letter page size
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Set the starting position for the address
    x = 0.5 * inch  # Adjust as needed for horizontal positioning
    y = height - 0.5 * inch  # Adjust as needed for vertical positioning

    # Process each address and draw it on the PDF
    print("Processing addresses...")
    for idx, row in df.iterrows():
        address = format_address_from_row(row)

        # Draw each line of the address
        current_y = y
        for line in address:
            c.drawString(x, current_y, line)
            current_y -= 0.3 * inch  # Move down for next line

        # Move to the next address position
        y -= 6.5 * inch  # Adjust this value to match the height of a #6 envelope

        # Check if we need to start a new page
        if y < 0:
            c.showPage()
            y = height - 0.5 * inch  # Reset y position for the new page

        print(f"Processed address {idx + 1}")

    c.save()
    print(f"Addresses saved to {output_path}")

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
