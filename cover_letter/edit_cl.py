import fitz  # PyMuPDF
import argparse

def edit_pdf(input_pdf_path, output_pdf_path, word_to_replace, replacement_word):
    # Open the original PDF
    pdf_document = fitz.open(input_pdf_path)

    # Loop through each page
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)  # get the page

        # Extract all the text instances (words)
        text_instances = page.search_for(word_to_replace)
        
        # Replace all instances of the word
        for inst in text_instances:
            # Get the rectangle surrounding the found word
            rect = inst

            # Erase the text in this area by drawing a white rectangle over it
            page.add_redact_annot(rect)
            page.apply_redactions()

            # Insert the new word at the position of the old word
            font = fitz.Font()  # Use the default font, or specify one if needed
            text_width = font.text_length(replacement_word, fontsize=12)
            
            x_shift = (len(replacement_word)-2)*4 # in order to prevent word wrapping
            x_center = (rect.x0 + (rect.width - text_width) / 2) + x_shift
            y_center = rect.y0 + (rect.height / 2) + (12 / 4)  + 1 # Adjust by 1/4th of font size for vertical centering

            page.insert_text((x_center, y_center), replacement_word, fontsize=12, color=(0, 0, 0))
            

    # Save the modified PDF with a new name
    pdf_document.save(output_pdf_path)
    pdf_document.close()

    
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Replace words in a PDF file.')

    # Add optional arguments with flags
    parser.add_argument('--input_pdf', nargs='?', default='TEST_CL.pdf', help='The path to the input PDF file')
    parser.add_argument('--company_name', required=True, help='Company name to replace XX with')    
    # parser.add_argument('--output_pdf', nargs='?', default='CL.pdf', help='The path to the output PDF file (with new name)')    
    parser.add_argument('--word_to_replace', nargs='?', default='XX,', help='The word to be replaced in the PDF')

    # Parse the arguments
    args = parser.parse_args()
    input_pdf = args.input_pdf
    company_name = args.company_name
    word_to_replace = args.word_to_replace
    
    output_pdf = f"{company_name}_CL.pdf"  # Custom name for the output PDF file
    
    edit_pdf(input_pdf, output_pdf, word_to_replace, company_name)
    print(f"PDF saved as: {output_pdf}")

