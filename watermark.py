from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm, inch
from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse
import os
import math

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path to the top level folder where documents are stored.")
parser.add_argument("--text", help="Watermark text", type=str, default="Watermark")
args = parser.parse_args()

def generate_watermark(name, landscape=False):
  c = canvas.Canvas(name)

  if landscape:
    #c.setPageSize((legal[1], legal[0]))
    c.setPageSize((10*inch,5.63*inch))
  else:
    c.setPageSize(letter)
    
  c.setFontSize(22)
  c.setFont('Helvetica-Bold', 36)
  c.setFillColorRGB(0.5, 0.5, 0.5, 0.4)

  midx = c._pagesize[0] / 2
  midy = c._pagesize[1] / 2
  
  c.drawCentredString(midx, midy, args.text)

  c.save()

generate_watermark('watermark.pdf', False)
generate_watermark('watermark_landscape.pdf', True)

watermark = PdfFileReader(open("watermark.pdf", "rb"))
watermark_landscape = PdfFileReader(open("watermark_landscape.pdf", "rb"))

def add_watermark(input_file_name, output_file_name):
  output_file = PdfFileWriter()
  input_file = PdfFileReader(open(input_file_name, "rb"))

  # Check page dimensions
  dims = input_file.getPage(0).mediaBox
  
  if dims.getWidth() > dims.getHeight():
    wm_page = watermark_landscape.getPage(0)
  else:
    wm_page = watermark.getPage(0)

  # Iterate over pages
  page_count = input_file.getNumPages()
  for page_number in range(page_count):
    # Get the page
    input_page = input_file.getPage(page_number)

    # Merge the watermark
    input_page.mergePage(wm_page)

    # Add the combined page to the output PDF
    output_file.addPage(input_page)

  # Write to disk
  with open(output_file_name, "wb") as outputStream:
    output_file.write(outputStream)

print("The following files will be replaced:")
for subfolder_path in [x[0] for x in os.walk(args.path)]:
  for file in os.listdir(subfolder_path):
    if file.endswith(".pdf"):
      print("- " + file)
      
user_ok = input("Are you sure you want to continue? Type YES: ")
if user_ok != "YES":
  exit()

print("Working...")
for subfolder_path in [x[0] for x in os.walk(args.path)]:
  for file in os.listdir(subfolder_path):
    if file.endswith(".pdf"):
      input_file_name = subfolder_path + '/'+ file
      output_file_name = subfolder_path + '/'+ file.split('.pdf')[0] + ' (watermarked).pdf'
      #print(input_file_name + ' ' + output_file_name)
      add_watermark(input_file_name, output_file_name)
      os.unlink(input_file_name)
      