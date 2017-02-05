import sys, getopt
import os

def getFileNameWithoutExtension(path):
  return os.path.splitext(os.path.basename(path))[0]

def main(argv):
	#load files
	sourcesile = ''
	templatefile = ''
	outpath = ''
	engineroot = ''
	try:
		opts, args = getopt.getopt(argv,"hs:t:d:e:",["source=","template=","outpath=", "engineroot="])
	except getopt.GetoptError:
		print 'test.py -s <sourcesile> -t <templatefile>'
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -s <sourceFile> -t <templatefile>'
			sys.exit()
		elif opt in ("-s", "--source"):
			sourcesile = arg
		elif opt in ("-t", "--template"):
			templatefile = arg
		elif opt in ("-d", "--outpath"):
			outpath = arg
		elif opt in ("-e", "--engineroot"):
			engineroot = arg	
	print 'Source file is ', sourcesile
	print 'Template file is ', templatefile
	print 'Output folder is ', templatefile

	#working with relative paths from sources to engine.

	outputfile = getFileNameWithoutExtension(sourcesile) + '.html'
	if len(outpath)>0:
		outputfile = os.path.join(outpath, outputfile)
		if not os.path.isdir(outpath):
			os.makedirs(outpath)	

	engine_absolute_path = os.getcwd()+'/'+engineroot
	lectures_absolute_path = os.getcwd()+'/'+sourcesile
	output_absolute_path = os.path.dirname(os.path.abspath(outputfile))
	output_to_engine_relative = os.path.relpath(engine_absolute_path, output_absolute_path) + '/'
	output_to_lectures_relative = os.path.relpath(lectures_absolute_path, output_absolute_path)

	#update template, save to output

	replacements = {'{{SourceName}}':output_to_lectures_relative, '{{enginePath}}':output_to_engine_relative}

	with open(templatefile) as infile, open(outputfile, 'w') as outfile:
	    for line in infile:
	        for src, target in replacements.iteritems():
	            line = line.replace(src, target)
	        outfile.write(line)

if __name__ == "__main__":
   main(sys.argv[1:])