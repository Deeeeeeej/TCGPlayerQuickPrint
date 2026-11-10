import os
import re


IMB_PATTERN = re.compile(r"[ADFT]{65}")


def get_most_recent_packing_slip(directory):
    files = [
        name
        for name in os.listdir(directory)
        if name.startswith("TCGplayer_PackingSlips_") and name.lower().endswith(".pdf")
    ]
    if not files:
        return None

    return max(files, key=lambda name: os.path.getmtime(os.path.join(directory, name)))

def get_most_recent_tcgplayer_input(directory, use_new_imb_mode=None):
    if use_new_imb_mode is True:
        packing_slip = get_most_recent_packing_slip(directory)
        return ("packing_slip", packing_slip) if packing_slip else (None, None)

    files = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue

        if name.startswith("TCGplayer_PackingSlips_") and name.lower().endswith(".pdf"):
            kind = "packing_slip"
        elif name.lower().endswith(".csv") and (
            name.startswith(("TCGplayer_ShippingExport_", "_TCGplayer_"))
            or use_new_imb_mode is False and name.startswith("TCGplayer_")
        ):
            kind = "csv"
        else:
            continue

        files.append((os.path.getmtime(path), kind, name))

    if not files:
        return None, None

    if use_new_imb_mode is False:
        files = [file for file in files if file[1] == "csv"]
        if not files:
            return None, None

    _, kind, name = max(files, key=lambda file: file[0])
    return kind, name


def extract_packing_slip_orders(pdf_path):
    import fitz

    orders = []
    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            lines = [line.strip() for line in page.get_text().splitlines() if line.strip()]
            imb_indexes = [index for index, line in enumerate(lines) if IMB_PATTERN.fullmatch(line)]
            if len(imb_indexes) != 1:
                raise ValueError(
                    f"Expected one 65-bar IMB on packing-slip page {page_number}; found {len(imb_indexes)}."
                )

            imb_index = imb_indexes[0]
            try:
                fold_index = lines.index("Fold Line", imb_index + 1)
            except ValueError as error:
                raise ValueError(
                    f"Could not find the address block on packing-slip page {page_number}."
                ) from error

            address = lines[imb_index + 1 : fold_index]
            if not address:
                raise ValueError(f"No address found on packing-slip page {page_number}.")

            orders.append((address, lines[imb_index]))

    return orders


def draw_imb(canvas, code, x, baseline_y):
    if not IMB_PATTERN.fullmatch(code):
        raise ValueError("An IMB must contain exactly 65 A, D, F, or T bars.")

    bar_width = 1.5
    bar_pitch = 3.12
    bar_dimensions = {
        "A": (baseline_y, 7.0),
        "D": (baseline_y - 3.5, 3.5),
        "F": (baseline_y - 3.5, 10.5),
        "T": (baseline_y, 3.5),
    }

    for symbol in code:
        bar_y, bar_height = bar_dimensions[symbol]
        canvas.rect(x, bar_y, bar_width, bar_height, stroke=0, fill=1)
        x += bar_pitch
