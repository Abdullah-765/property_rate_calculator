# pdf_export.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
import textwrap

# ===========================
# Layout Constants
# ===========================
PAGE_WIDTH, PAGE_HEIGHT = A4
LEFT_MARGIN = 30 * mm
RIGHT_MARGIN = 30 * mm
TOP_MARGIN = 30 * mm

LINE_HEIGHT = 18
DATA_LINE_HEIGHT = 24
SECTION_BREAK_GAP = 20


def generate_pdf(pages: list) -> BytesIO:
    """
    Generates a multi-page PDF.
    `pages` is a list of dicts, each dict representing a page.
    Each dict can have keys:
    - 'Category' (e.g., "Filer", "Non-Filer", "Late Filer")
    - 'Property Address' (optional)
    - Other key-value pairs for buyer/seller sections
    - '__BUYER_SECTION__' and '__SELLER_SECTION__' to mark sections
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    for page_data in pages:
        y = PAGE_HEIGHT - TOP_MARGIN

        # ===========================
        # MAIN HEADING
        # ===========================
        c.setFont("Times-Bold", 22)
        c.drawCentredString(PAGE_WIDTH / 2, y, "TRANSFER EXPENSE SHEET")
        y -= 8
        c.line(PAGE_WIDTH / 4, y, PAGE_WIDTH * 3 / 4, y)
        y -= 30

        # ===========================
        # CATEGORY TYPE
        # ===========================
        category = page_data.get("Category")
        if category:
            c.setFont("Times-Bold", 16)
            c.drawCentredString(PAGE_WIDTH / 2, y, category.upper())
            y -= 25

        # ===========================
        # PROPERTY ADDRESS
        # ===========================
        address = page_data.get("Property Address")
        if address:
            c.setFont("Times-Bold", 16)
            for line in textwrap.wrap(address, width=50):
                c.drawCentredString(PAGE_WIDTH / 2, y, line)
                y -= LINE_HEIGHT
            y -= 10
            c.line(PAGE_WIDTH / 4, y, PAGE_WIDTH * 3 / 4, y)
            y -= 25

        # ===========================
        # MAIN CONTENT
        # ===========================
        for label, value in page_data.items():

            if label in ["Category", "Property Address"]:
                continue

            # -----------------------
            # BUYER SECTION
            # -----------------------
            if label == "__BUYER_SECTION__":
                y -= SECTION_BREAK_GAP
                c.setFont("Times-Bold", 16)
                c.drawCentredString(PAGE_WIDTH / 2, y, "BUYER EXPENSES")
                y -= 5
                c.line(LEFT_MARGIN, y, PAGE_WIDTH - RIGHT_MARGIN, y)
                y -= DATA_LINE_HEIGHT
                continue

            # -----------------------
            # SELLER SECTION
            # -----------------------
            if label == "__SELLER_SECTION__":
                y -= SECTION_BREAK_GAP
                c.setFont("Times-Bold", 16)
                c.drawCentredString(PAGE_WIDTH / 2, y, "SELLER EXPENSES")
                y -= 5
                c.line(LEFT_MARGIN, y, PAGE_WIDTH - RIGHT_MARGIN, y)
                y -= DATA_LINE_HEIGHT
                continue

            # -----------------------
            # FONT LOGIC
            # -----------------------
            if "Total" in label:
                c.setFont("Times-Bold", 14)
            else:
                c.setFont("Times-Roman", 12)

            if "Services Charges" in label:
                y -= SECTION_BREAK_GAP
                c.setFont("Times-Bold", 14)
                y -= 5


            text = f"{label}: {value}"
            wrapped_lines = textwrap.wrap(text, width=90)

            for line in wrapped_lines:
                if y < 50:  # start new page if space runs out
                    c.showPage()
                    y = PAGE_HEIGHT - TOP_MARGIN
                    c.setFont("Times-Roman", 12)

                c.drawString(LEFT_MARGIN, y, line)
                y -= DATA_LINE_HEIGHT

            y -= 6

        # ===========================
        # End of page
        # ===========================
        c.showPage()

    # ===========================
    # Save PDF
    # ===========================
    c.save()
    buffer.seek(0)
    return buffer
