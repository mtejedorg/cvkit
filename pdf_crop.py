"""Crop a headless-Edge-rendered single-page PDF down to its actual content height.

compile_all_pdfs.py renders each CV/cover letter onto one deliberately
oversized page (see OVERSIZED_PAGE_HEIGHT_MM in that file) so content can
never spill onto a second page. This module finds where the real content
ends and crops the page down to that height plus a small margin, removing
the trailing whitespace that a fixed/guessed page height otherwise leaves.
"""

import os
import fitz  # PyMuPDF

MM_TO_PT = 2.8346456693


def crop_pdf_to_content(pdf_path, bottom_margin_mm=15.0, min_height_mm=80.0, max_ratio=0.9):
    """Crop page 1 of pdf_path down to its content height, in place.

    Returns the final page height in mm.

    Raises ValueError (leaving the PDF uncropped) if the detected content
    height comes within max_ratio of the oversized canvas height, since
    that means either a stray drawing/bbox threw off the measurement or
    the document genuinely needs more than the oversized bound allows -
    either way, silently cropping to a bad value is worse than leaving
    the PDF as rendered and surfacing the problem.
    """
    doc = fitz.open(pdf_path)
    try:
        page = doc[0]
        oversized_height_pt = page.rect.height

        max_y = 0.0

        for block in page.get_text("blocks"):
            max_y = max(max_y, block[3])  # y1 of each text block

        for drawing in page.get_drawings():
            rect = drawing.get("rect")
            if rect:
                max_y = max(max_y, rect.y1)

        for info in page.get_image_info():
            bbox = info.get("bbox")
            if bbox:
                max_y = max(max_y, bbox[3])

        content_height_pt = max_y + bottom_margin_mm * MM_TO_PT

        if content_height_pt > oversized_height_pt * max_ratio:
            raise ValueError(
                f"content height ~{content_height_pt / MM_TO_PT:.0f}mm is too close to "
                f"the oversized canvas ({oversized_height_pt / MM_TO_PT:.0f}mm); "
                f"left uncropped for manual review"
            )

        content_height_pt = max(content_height_pt, min_height_mm * MM_TO_PT)

        # Only the CropBox is changed (not the MediaBox): viewers and print
        # pipelines render/paginate to the CropBox, and leaving MediaBox
        # alone avoids PyMuPDF's cross-validation between the two boxes
        # (setting both against inconsistent internal coordinate state
        # raises "CropBox not in MediaBox").
        new_rect = fitz.Rect(0, 0, page.rect.width, content_height_pt)
        page.set_cropbox(new_rect)

        try:
            doc.saveIncr()
        except Exception:
            tmp_path = pdf_path + ".tmp"
            doc.save(tmp_path)
            doc.close()
            os.replace(tmp_path, pdf_path)
            return content_height_pt / MM_TO_PT

        return content_height_pt / MM_TO_PT
    finally:
        if not doc.is_closed:
            doc.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python pdf_crop.py <path-to-pdf>")
        sys.exit(1)

    final_height = crop_pdf_to_content(sys.argv[1])
    print(f"Cropped to {final_height:.1f}mm content height")
