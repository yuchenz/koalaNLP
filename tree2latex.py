#!/usr/bin/python2.7

import codecs, re, sys

def outputHead(outf):
	head = '''\documentclass[a4paper, landscape]{article}
\usepackage[margin=0.55in]{geometry}
\usepackage{color}
%\usepackage{qtree}
\usepackage{tikz}
\usepackage{tikz-qtree}
\usepackage{CJK}

\\begin{document}

\\begin{CJK*}{UTF8}{gbsn}\n\n'''
	outf.write(head)

def outputTail(outf):
	tail = '''

\end{CJK*}

\end{document}
	'''
	outf.write(tail)

def convert(inf, outf):
	outputHead(outf)
	for i, line in enumerate(inf):
		outf.write("\n\nSent \\#" + str(i) + '\n\n')
		scale = min(1, 400.0/len(line))
		outf.write('\\begin{tikzpicture}[ultra thick, scale='+str(scale)+']\n\Tree ')
		line = re.sub('\(', '[.', line)
		line = re.sub('\[. ', '[ ', line)
		line = re.sub('\)', ' ]', line)
		outf.write(line)
		outf.write('\end{tikzpicture}\n\n')
		outf.write('\clearpage')
	outputTail(outf)
	outf.close()

if __name__ == "__main__":
	inf = codecs.open(sys.argv[1], 'r', 'utf-8')
	outf = codecs.open(sys.argv[2], 'w', 'utf-8')

	convert(inf, outf)
