"""Fix the Chrome PDF to exact print geometry and impose an A4 test sheet.

business-card-print.pdf: 2 pages (front, back), 69 x 94 mm each, TrimBox 63 x 88 mm, BleedBox = MediaBox.
business-card-a4-sheet.pdf: A4, 3 x 3 cards cut to trim, front page then back page (mirrored columns for long-edge duplex), with cut marks.
"""
import sys
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from pypdf.generic import RectangleObject, DecodedStreamObject

MM = 72 / 25.4
W, H, BLEED = 69 * MM, 94 * MM, 3 * MM
TW, TH = 63 * MM, 88 * MM

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

# A4 imposition, cards cut to trim and placed edge to edge
AW, AH = 210 * MM, 297 * MM
ox, oy = (AW - 3 * TW) / 2, (AH - 3 * TH) / 2
sheet = PdfWriter()
for side, card in enumerate(cards):
    pg = PageObject.create_blank_page(width=AW, height=AH)
    for r in range(3):
        for c in range(3):
            col = c if side == 0 else 2 - c  # mirror columns on the back for long-edge duplex
            x, y = ox + col * TW - BLEED, oy + r * TH - BLEED
            clip = PageObject.create_blank_page(width=W, height=H)
            clip.merge_page(card)
            clip.cropbox = clip.mediabox = RectangleObject([BLEED, BLEED, W - BLEED, H - BLEED])
            pg.merge_transformed_page(clip, Transformation().translate(x, y), over=True)
    # cut marks in the margins, 2 mm away from the card block
    gap, ops = 2 * MM, ["q 0 G 0.3 w"]
    for i in range(4):
        x = ox + i * TW
        ops += [f"{x:.2f} 0 m {x:.2f} {oy - gap:.2f} l S", f"{x:.2f} {oy + 3 * TH + gap:.2f} m {x:.2f} {AH:.2f} l S"]
        y = oy + i * TH
        ops += [f"0 {y:.2f} m {ox - gap:.2f} {y:.2f} l S", f"{ox + 3 * TW + gap:.2f} {y:.2f} m {AW:.2f} {y:.2f} l S"]
    ops.append("Q")
    marks = PageObject.create_blank_page(width=AW, height=AH)
    stream = DecodedStreamObject()
    stream.set_data("\n".join(ops).encode())
    marks.replace_contents(stream)
    pg.merge_page(marks)
    sheet.add_page(pg)
sheet.write("business-card-a4-sheet.pdf")
print("ok")
