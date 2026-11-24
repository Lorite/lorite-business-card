"""Fix the Chrome PDF to exact print geometry and impose an A4 sheet.

business-card-print.pdf: 91 x 61 mm page, TrimBox 85 x 55 mm, BleedBox = MediaBox (for a print shop).
business-card-a4-sheet.pdf: A4 with 2 x 5 cards cut to trim, with cut marks (for an office printer and a paper cutter).
"""
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from pypdf.generic import RectangleObject, DecodedStreamObject

MM = 72 / 25.4
BLEED = 3 * MM
TW, TH = 85 * MM, 55 * MM
W, H = TW + 2 * BLEED, TH + 2 * BLEED
COLS, ROWS = 2, 5

src = PdfReader("business-card-print.pdf")
out = PdfWriter()
cards = []
for page in src.pages:
    pw, ph = float(page.mediabox.width), float(page.mediabox.height)
    new = PageObject.create_blank_page(width=W, height=H)
    new.merge_transformed_page(page, Transformation().scale(W / pw, H / ph))
    new.bleedbox = RectangleObject([0, 0, W, H])
    new.trimbox = RectangleObject([BLEED, BLEED, W - BLEED, H - BLEED])
    out.add_page(new)
    cards.append(new)
out.write("business-card-print.pdf")

AW, AH = 210 * MM, 297 * MM
ox, oy = (AW - COLS * TW) / 2, (AH - ROWS * TH) / 2
sheet = PdfWriter()
for side, card in enumerate(cards):
    pg = PageObject.create_blank_page(width=AW, height=AH)
    for r in range(ROWS):
        for c in range(COLS):
            col = c if side == 0 else COLS - 1 - c  # mirror columns on a back side for long-edge duplex
            clip = PageObject.create_blank_page(width=W, height=H)
            clip.merge_page(card)
            clip.cropbox = clip.mediabox = RectangleObject([BLEED, BLEED, W - BLEED, H - BLEED])
            pg.merge_transformed_page(clip, Transformation().translate(ox + col * TW - BLEED, oy + r * TH - BLEED), over=True)
    gap, ops = 2 * MM, ["q 0 G 0.3 w"]
    for i in range(COLS + 1):
        x = ox + i * TW
        ops += [f"{x:.2f} 0 m {x:.2f} {oy - gap:.2f} l S", f"{x:.2f} {oy + ROWS * TH + gap:.2f} m {x:.2f} {AH:.2f} l S"]
    for i in range(ROWS + 1):
        y = oy + i * TH
        ops += [f"0 {y:.2f} m {ox - gap:.2f} {y:.2f} l S", f"{ox + COLS * TW + gap:.2f} {y:.2f} m {AW:.2f} {y:.2f} l S"]
    ops.append("Q")
    marks = PageObject.create_blank_page(width=AW, height=AH)
    stream = DecodedStreamObject()
    stream.set_data("\n".join(ops).encode())
    marks.replace_contents(stream)
    pg.merge_page(marks)
    sheet.add_page(pg)
sheet.write("business-card-a4-sheet.pdf")
print("ok")
