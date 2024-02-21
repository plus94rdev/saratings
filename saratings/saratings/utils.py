import mammoth

def convert_docx_to_html(docx_path):

    with open(docx_path, "rb") as docx_file:

        result = mammoth.convert_to_html(docx_file)
        
        html = result.value  # The generated HTML
        
        return html