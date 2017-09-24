import os, subprocess, sys, time, shutil
from PyPDF2 import PdfFileReader, PdfFileWriter, utils
from cStringIO import StringIO
import random

path = "ToMerge/"
sys.stdout = sys.__stdout__

def decompress_pdf(temp_buffer):
    temp_buffer.seek(0)  # Make sure we're at the start of the file.
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
	file = "ToMerge/" + str(file.replace(" ", "\ "))
	if file[-3:] != 'pdf' and file[-10:] !='.gitignore':
		command = "unoconv -f pdf " + str(file)
		try:
			print "  converting to PDF... :", file
			command  += "; mv " + str(file) + " Consumed/"
			subprocess.call(command, shell=True)
		except:
			print "Error while converting ", file, " to PDF"
	elif file[-3:] == 'pdf':
		try:
			command = "cp " + str(file) + " Consumed/"
			subprocess.call(command, shell=True)
		except:
			pass
 
to_merge = os.listdir(path)
list_files.sort()
for file in to_merge:
	time.sleep(1)
	file = "ToMerge/" + str(file.replace("  ", "\ "))
	if file[-3:] == 'pdf' and file[9] != '~':	
		with open(file, 'rb') as input_file:
			input_buffer = StringIO(input_file.read())
		try:
			print "   appending file...   :", file
			append_pdf(PdfFileReader(input_buffer),output)
		except utils.PdfReadError:
			try:
				print "decompressing pdf  : ", file
				append_pdf(PdfFileReader(decompress_pdf(input_buffer)),output)
			except:
				pass


# Writing all the collected pages to a file
hash = random.getrandbits(128)
output_file = "Output/Combined" + str(hash)[:6] + str(".pdf")
output.write(open(output_file,"wb"))
print "   Generated PDF  : ", output_file
for the_file in os.listdir(path):
    file_path = os.path.join(path, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)
