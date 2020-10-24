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


def remove_pages(source_pdf, pages_to_delete):
    """
    Remove one or more pages (as specified in the input array) from a single PDF file.
    Any potential bookmarks from the source file will be lost.
    """
    source = PyPDF2.PdfFileReader(open(source_pdf, 'rb'))
    output = PyPDF2.PdfFileWriter()
    pages_to_delete = [page-1 for page in pages_to_delete]  # start from 0 instead of 1
    for i in range(source.getNumPages()):
        if i not in pages_to_delete:
            output.addPage(source.getPage(i))
    with open(f'cleaned_{source_pdf}', 'wb') as f:
        output.write(f)


def find_files_with_extension(ext):
    """
    Helper function to get a list of files present in the current directory with the desired file extension.
    Example: 
    pdfs = find_files_with_extension('.pdf')
    """
    from glob import glob
    return glob("*.pdf")





if __name__ == "__main__":
    ### SAMPLE USAGE ###
    # rotate_specific_pages(source_pdf='dummy.pdf', output_pdf='rotated.pdf', pages=(1,), clockwise_degree=90)
    # merge(['dummy.pdf', 'rotated.pdf'], output_pdf='merged.pdf')
    # add_watermark(source_pdf='merged.pdf', watermark_pdf='watermark.pdf', output_pdf='watermarked.pdf')
    remove_pages(source_pdf='merged.pdf', pages_to_delete=[1])
