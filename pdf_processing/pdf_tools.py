"""
Idea based on "Complete Python Developer in 2020: Zero to Mastery" from Andrei Neagoie.
"""

import PyPDF2


def rotate_specific_pages(source_pdf, output_pdf, pages, clockwise_degree):
    """Rotate the specified pages of 'source_pdf' (str) by 'clockwise_degree' (int, increment of 90)
    and save to 'output_pdf' (str). Input 'pages' can be either 'all' or a list of integers.
    """
    assert clockwise_degree % 90 == 0
    with open(source_pdf, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        writer = PyPDF2.PdfFileWriter()
        for i in range(reader.getNumPages()):
            page = reader.getPage(i)
            if pages == 'all':
                page.rotateClockwise(clockwise_degree)
            else:
                if i+1 in pages:
                    page.rotateClockwise(clockwise_degree)
            writer.addPage(page)
        with open(output_pdf, 'wb') as new_file:
            writer.write(new_file)


def merge(list_of_pdfs, output_pdf):
    """Merge (concatenate) the pdf files named in 'list_of_pdfs' and output to 'output_pdf'."""
    merger = PyPDF2.PdfFileMerger()
    for pdf in list_of_pdfs:
        merger.append(pdf)
    merger.write(output_pdf)


def add_watermark(source_pdf, watermark_pdf, output_pdf):
    """Add a watermark (single page 'watermark_pdf') to 'source_pdf' and output to 'output_pdf'."""
    template = PyPDF2.PdfFileReader(open(source_pdf, 'rb'))
    watermark = PyPDF2.PdfFileReader(open(watermark_pdf, 'rb'))
    output = PyPDF2.PdfFileWriter()
    for i in range(template.getNumPages()):
        page = template.getPage(i)
        page.mergePage(watermark.getPage(0))
        output.addPage(page)
    with open(output_pdf, 'wb') as file:
        output.write(file)


if __name__ == "__main__":
    ### SAMPLE USAGE ###
    rotate_specific_pages(source_pdf='dummy.pdf', output_pdf='rotated.pdf', pages=(1,), clockwise_degree=90)
    # merge(['dummy.pdf', 'rotated.pdf'], output_pdf='merged.pdf')
    # add_watermark(source_pdf='merged.pdf', watermark_pdf='watermark.pdf', output_pdf='watermarked.pdf')
