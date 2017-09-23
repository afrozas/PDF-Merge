# Loading the pyPdf Library
import os, subprocess, sys
from PyPDF2 import PdfFileReader, PdfFileWriter, utils
from cStringIO import StringIO

path = "/home/enigmaeth/Code/PDFMerge/ToMerge"
sys.stdout = sys.__stdout__

def decompress_pdf(temp_buffer):
    temp_buffer.seek(0)  # Make sure we're at the start of the file.
 #    sys.stdout = os.fdopen(outfd, 'w')
	# sys.stderr = os.fdopen(errfd, 'w')
    process = subprocess.Popen(['pdftk.exe',
                                '-',  # Read from stdin.
                                'output',
                                '-',  # Write to stdout.
                                'uncompress'],
                                stdin=temp_buffer,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return StringIO(stdout)

# Creating a routine that appends files to the output file
def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


list_files = os.listdir(path)
# Creating an object where pdf pages are appended to
output = PdfFileWriter()

# Appending two pdf-pages from two different files
for file in list_files:
	file = "ToMerge/" + file
	if file[-3:] != 'pdf':
		command = "unoconv -f pdf " + str(file.replace(" ", "\ "))
		try:
			subprocess.call(command, shell=True)
		except:
			print "Error while converting ", file, " to PDF"

	with open(file, 'rb') as input_file:
		input_buffer = StringIO(input_file.read())

	try:
		print " appending file ", file, "..."
		append_pdf(PdfFileReader(input_buffer),output)
	except utils.PdfReadError:
		#append_pdf(PdfFileReader(decompress_pdf(input_buffer)),output)
		print " [Error while appending] skiping file ", file, "..." 
		pass

# Writing all the collected pages to a file
output.write(open("CombinedPages.pdf","wb"))