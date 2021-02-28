# automate_watermark
Loops through subdirectories and watermarks all PDFs that it can find

## Instructions

1. Run `pip install -r requirements.txt` to install dependencies
1. Launch tool with:
`python watermark.py <PATH TO FOLDER> --text <WATERMARK TEXT>`
1. The tool will prompt you with the files it plans to replace

## Known Issues

- Does not handle unusual page sizes well
- Crashes if there is a video embedded in the PDF