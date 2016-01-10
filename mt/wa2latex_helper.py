"""
Yuchen Zhang
03/24/2015
"""

import sys
import codecs

latex_pre=r"""\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[top=0.2in, left=0.2in, right=0.2in, bottom=0.55in]{geometry}
\usepackage{color}
\usepackage{CJK}
\usepackage{tikz}

\begin{document}

\begin{CJK*}{UTF8}{gbsn}

\newcommand\myscale{}
\newcommand\enwordnum{}
\newcommand\chwordnum{}
\newcommand\chidwords{}
\newcommand\enidwords{}
\newcommand\correctwa{}
\newcommand\missedwa{}
\newcommand\extrawa{}

\newcommand\myminisize{}
\newcommand\mywordscale{}

\newcommand{\mydrawwordalignmentmatrix}[8]{

	\renewcommand\myminisize{#1 * 1}
	\renewcommand\mywordscale{\myminisize * 1.8}

	\iffalse
	The parameters are:\\
	scale: #1\\ \# English words: #2\\ \# Chinese words: #3\\

	Chinese words are:\\
	\foreach \x/\y in #4 {\x -- \y\\}

	English words are:\\
	\foreach \x/\y in #5 {\x -- \y\\}

	correct word alignments are: (en-ch) \\
	\foreach \x/\y in #6 {\x -- \y\\}

	missed word alignments are: (en-ch) \\
	\foreach \x/\y in #7 {\x -- \y\\}

	extra word alignments are: (en-ch) \\
	\foreach \x/\y in #8 {\x -- \y\\}
	\fi

	\begin{tikzpicture}[
	correct/.style={rectangle,fill=black!80,minimum size=\myminisize cm},
	missed/.style={rectangle,fill=yellow!50,minimum size=\myminisize cm},
	extra/.style={rectangle,fill=gray!50,minimum size=\myminisize cm},
	chword/.style={left, scale=\mywordscale},
	enword/.style={right, rotate=60, scale=\mywordscale},
	scale=#1]

	\draw[draw=gray] (0,0) grid (#2,#3);

	\foreach \y/\f in #4 {
	\node[chword] at (-.2,#3-.5-\y) {{\f}};
	}

	\foreach \x/\e in #5 {
	\node[enword] at (\x+.3,#3+.2) {{\e}};
	}

	% draw correct word alignment
	\foreach \x/\y in #6 {
	\node[correct] at (\x+.5, #3-.5-\y) {};
	}

	% draw missed word alignment
	\foreach \x/\y in #7 {
	\node[missed] at (\x+.5, #3-.5-\y) {};
	}

	% draw extra word alignment
	\foreach \x/\y in #8 {
	\node[extra] at (\x+.5, #3-.5-\y) {};
	}
	\end{tikzpicture}}

"""

latex_post=r"""\end{CJK*}
\end{document}"""

latex_draw_matrix=r"""\mydrawwordalignmentmatrix{\myscale}{\enwordnum}{\chwordnum}{\chidwords}{\enidwords}{\correctwa}{\missedwa}{\extrawa}"""

