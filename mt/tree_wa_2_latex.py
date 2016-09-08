#!/usr/bin/python2.7

import codecs, re, sys

def outputHead(outf):
	head = '''\documentclass[a4paper, landscape]{article}
\usepackage[margin=0in]{geometry}
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

def construct_a_tree(line, symbol, direction):
	if direction == 'down':
		string = '\\begin{scope}[xshift=1in,frontier/.style={distance from root=470pt}]\n\Tree '
	elif direction == 'up':
		string = '\\begin{scope}[xshift=-1.5in,yshift=-14in, grow\'=up, frontier/.style={distance from root=470pt}]\n\Tree '

	line = re.sub('\(', '[.', line)
	line = re.sub('\[. ', '[ ', line)
	line = re.sub('\)', ' ]', line)
	
	line = line.split()
	cnt = 0
	for i in xrange(len(line) - 1):
		if line[i + 1] == ']' and line[i] != ']':
			line[i] = '\\node(%s%d){%s};' % (symbol, cnt, line[i])
			cnt += 1
	line = ' '.join(line)

	string += line
	string += '\n\end{scope}\n\n'

	return string

def construct_a_wa(wa_line):
	string = '\\begin{scope}[dashed]\n'
	for wa in wa_line.split():
		print wa
		e_i = int(wa.split('-')[0])
		f_i = int(wa.split('-')[1])
		string += '\draw (e%d)--(f%d);\n' %(e_i, f_i)
	string += '\end{scope}\n\n'
	return string

def convert(tree1f, tree2f, waf, outf):
	outputHead(outf)
	tree2_list = tree2f.readlines()
	wa_list = waf.readlines()
	for i, line1 in enumerate(tree1f):
		line2 = tree2_list[i]
		wa = wa_list[i]
		outf.write("\n\nSent \\#" + str(i) + '\n\n')
		scale = min(1, 400.0/len(line1), 400.0/len(line2))
		outf.write('\\begin{tikzpicture}[ultra thick, scale='+str(scale)+']\n')
		string_tree1 = construct_a_tree(line1, symbol='e', direction='down')
		string_tree2 = construct_a_tree(line2, symbol='f', direction='up')
		string_wa = construct_a_wa(wa)
		outf.write(string_tree1)
		outf.write(string_tree2)
		outf.write(string_wa)

	outf.write('\end{tikzpicture}\n\n')
	outputTail(outf)
	outf.close()

if __name__ == "__main__":
	tree1f = codecs.open(sys.argv[1], 'r', 'utf-8')
	tree2f = codecs.open(sys.argv[2], 'r', 'utf-8')
	waf = codecs.open(sys.argv[3], 'r', 'utf-8')
	outf = codecs.open(sys.argv[4], 'w', 'utf-8')

	convert(tree1f, tree2f, waf, outf)
