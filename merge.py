import os, subprocess, sys, shutil
from PyPDF2 import PdfFileReader, PdfFileWriter, utils
from cStringIO import StringIO
import random

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
list_files.sort()
# Appending two pdf-pages from two different files
for file in list_files:
	file = "ToMerge/" + file
	if file[-3:] != 'pdf' and file[-10:] !='.gitignore':
		command = "unoconv -f pdf " + str(file.replace(" ", "\ "))
		try:
			command  += "; mv " + str(file.replace(" ", "\ ")) + " Consumed/"
			subprocess.call(command, shell=True)
		except:
			print "Error while converting ", file, " to PDF"

	if file[-3:] == 'pdf' :
		with open(file, 'rb') as input_file:
			input_buffer = StringIO(input_file.read())
		try:
			print "   appending file...  :", file
			append_pdf(PdfFileReader(input_buffer),output)
		except utils.PdfReadError:
			#append_pdf(PdfFileReader(decompress_pdf(input_buffer)),output)
			print " [Error merging file] :", file , "skiping... " 
			pass

# Writing all the collected pages to a file
hash = random.getrandbits(128)
output_file = "Output/Combined" + str(hash)[:6] + str(".pdf")
output.write(open(output_file,"wb"))
print "   Generated PDF : ", output_file