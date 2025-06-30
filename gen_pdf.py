import argparse
import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.styles import get_style_by_name
from pygments.token import Token

def find_files(directory, extensions):
    """Find all files in a directory with the given extensions."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(tuple(extensions)):
                yield os.path.join(root, file)

def hex_to_rgb(hex_color):
    """Convert a hex color string to an (r, g, b) tuple."""
    if hex_color is None:
        return 0, 0, 0
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        return 0, 0, 0
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_pdf(files, output_filename):
    """Create a PDF from a list of files."""
    pdf = FPDF()
    pdf.set_auto_page_break(True, margin=15)
    
    style = get_style_by_name('colorful')
    default_text_color = hex_to_rgb(style.style_for_token(Token.Text)['color'])

    for filepath in files:
        pdf.add_page()
        
        # Add file metadata
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, f"File: {os.path.basename(filepath)}".encode('latin-1', 'replace').decode('latin-1'), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.set_font("Helvetica", 'I', 10)
        pdf.cell(0, 10, f"Path: {filepath}".encode('latin-1', 'replace').decode('latin-1'), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(10)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            try:
                lexer = get_lexer_by_name(os.path.splitext(filepath)[1].strip('.'))
            except:
                lexer = guess_lexer(code)

            pdf.set_font('Courier', '', 10)
            line_height = pdf.font_size * 1.25
            
            line_num = 1
            pdf.set_text_color(128, 128, 128) # Gray for line numbers
            pdf.cell(12, line_height, f"{line_num:4d} ", border=0, new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_text_color(*default_text_color)

            tokens = lexer.get_tokens(code)
            for ttype, tvalue in tokens:
                style_def = style.style_for_token(ttype)
                color = hex_to_rgb(style_def['color'])
                
                font_style = ''
                if style_def['bold']:
                    font_style += 'B'
                if style_def['italic']:
                    font_style += 'I'
                
                pdf.set_font('Courier', style=font_style, size=10)
                pdf.set_text_color(*color)
                
                lines = tvalue.split('\n')
                for i, line in enumerate(lines):
                    if line:
                        pdf.write(line_height, line.encode('latin-1', 'replace').decode('latin-1'))
                    if i < len(lines) - 1:
                        pdf.ln(line_height)
                        line_num += 1
                        pdf.set_text_color(128, 128, 128)
                        pdf.cell(12, line_height, f"{line_num:4d} ", border=0, new_x=XPos.RIGHT, new_y=YPos.TOP)
                        pdf.set_text_color(*color)
            
            pdf.set_text_color(*default_text_color)

        except Exception as e:
            pdf.set_font("Helvetica", '', 12)
            error_message = f"Error processing file {filepath}: {e}"
            pdf.multi_cell(0, 10, error_message.encode('latin-1', 'replace').decode('latin-1'))

    pdf.output(output_filename)
    print(f"Successfully generated {output_filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate a PDF from source code files with syntax highlighting.")
    parser.add_argument("directory", help="The directory to scan for source code files.")
    parser.add_argument("-o", "--output", default="output.pdf", help="The name of the output PDF file.")
    parser.add_argument("-e", "--extensions", nargs='+', required=True, help="A list of file extensions to include (e.g., .py .js .html).")
    
    args = parser.parse_args()
    
    files_to_process = list(find_files(args.directory, args.extensions))
    
    if not files_to_process:
        print("No files found with the specified extensions.")
        return
        
    create_pdf(files_to_process, args.output)

if __name__ == "__main__":
    main()
