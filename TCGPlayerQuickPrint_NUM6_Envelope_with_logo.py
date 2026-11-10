import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from imb_envelope import draw_imb, extract_packing_slip_orders, get_most_recent_tcgplayer_input

USE_NEW_IMB_MODE = None
LOGO_FILENAME = "logo.jpg"

def draw_sender_block(c, logo_path, env_height):
    logo = ImageReader(logo_path)
    image_width, image_height = logo.getSize()
    logo_width = 1.5 * inch
    logo_height = logo_width * image_height / image_width
    left_margin = 0.25 * inch
    logo_top = env_height - 0.25 * inch
    logo_bottom = logo_top - logo_height

    c.drawImage(logo, left_margin, logo_bottom, width=logo_width, height=logo_height, mask='auto')
    c.setFont("Helvetica", 12)
    first_address_y = logo_bottom - 0.05 * inch - 14
    c.drawString(left_margin + 1, first_address_y, "PO Box 262")
    c.drawString(left_margin + 1, first_address_y - 0.2 * inch, "Andover, KS 67002")


def get_most_recent_tcgplayer_csv(directory):
    """Fetch the most recent TCGPlayer CSV file from a given directory."""
    
    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Filter out files that don't match the TCGPlayer CSV naming pattern
    tcgplayer_files = [f for f in files if f.startswith(('TCGplayer_', '_TCGplayer_')) and f.endswith('.csv')]

    if not tcgplayer_files:
        return None

    # Sort the files by last modified date
    sorted_files = sorted(tcgplayer_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

    # Return the most recently modified file
    return os.path.join(directory, sorted_files[0])


def create_pdf_from_csv(csv_path, output_path, logo_path):
    """Generate a PDF with one address per page for #6 envelopes, with logo, business address in the top left, and lowered recipient address."""
    
    # Read the CSV data into a DataFrame
    df = pd.read_csv(csv_path)

    # Envelope dimensions for landscape orientation
    env_width = 6.5 * inch  # 6 1/2 inches (width)
    env_height = 4 * inch  # 3 5/8 inches (height)

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

        draw_sender_block(c, logo_path, env_height)

        # Drop the recipient address by two lines
        drop_lines = 2
        y_position_start = (env_height + text_block_height) / 2 - (line_height * drop_lines)

        for line in address:
            line = str(line)
            # Center each line of the address horizontally
            text_width = c.stringWidth(str(line), 'Helvetica', font_size)
            x_position = (env_width - text_width) / 2

            c.drawString(x_position, y_position_start, line)
            y_position_start -= line_height  # Move down for the next line

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

def create_pdf_from_packing_slips(pdf_path, output_path, logo_path):
    orders = extract_packing_slip_orders(pdf_path)
    env_width = 6.5 * inch
    env_height = 4 * inch
    font_size = 12
    line_height = 14
    c = canvas.Canvas(output_path, pagesize=(env_width, env_height))

    for index, (address, imb) in enumerate(orders):
        draw_sender_block(c, logo_path, env_height)

        text_block_height = len(address) * line_height
        y_position = (env_height + text_block_height) / 2 - line_height * 2
        for line in address:
            c.drawCentredString(env_width / 2, y_position, str(line))
            y_position -= line_height

        draw_imb(c, imb, (env_width - (64 * 3.12 + 1.5)) / 2, y_position)
        if index < len(orders) - 1:
            c.showPage()

    c.save()


downloads_folder = os.path.expanduser('~/Downloads')
input_type, input_name = get_most_recent_tcgplayer_input(downloads_folder, USE_NEW_IMB_MODE)
if input_name:
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_directory, 'addresses.pdf')
    input_path = os.path.join(downloads_folder, input_name)
    if input_type == "packing_slip":
        logo_path = os.path.join(script_directory, LOGO_FILENAME)
        create_pdf_from_packing_slips(input_path, output_path, logo_path)
    else:
        logo_path = os.path.join(script_directory, LOGO_FILENAME)
        create_pdf_from_csv(input_path, output_path, logo_path)
else:
    print("No matching TCGplayer shipping export or packing-slip PDF found.")
