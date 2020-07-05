# pdf-question-paper-image-parser

This python code reads a question paper document in PDF format, converts the images to string of charecters using pytesseract and extracts all the questions along with its answers. The parsed data is then stored into a JSON file.

## Dependencies
* pytesseract
* minecart

## Usage 

```console
foo@bar:~$ python extract_mcqs.py test.pdf 298
```
arguments: 
* filename 
* total no of pages
