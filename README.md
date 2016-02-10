# koalaNLP
Useful NLP scripts

 - processCH.py
   
   Chinese data statistics and cleaning processor
 
 - line2tree.py

   convert string format parse trees in a file into tree format ones in standard output, or
   
   convert a string format parse tree from standard input into a tree format one in standard output

 - mergeSort2F.py 

   merge two sorted files into one sorted file

 - isLegalTree.py

   check if trees from stdin are legal trees that can be parsed by nltk.Tree

### for MT
 - mt/parallelSents.py
   
   wholeFile and wholeParaFile are sentence level parallel files, one sentence per line; partFile contains a part of the sentences in wholeFile; select the according parallel sentences in wholeParaFile into partParaFile

 - mt/wa2latex.py

   given foreign sentences file, English sentences file, gold word alignemnt file, auto word alignment file, all sentence aligned (one sentence per line), output a .tex file which generates a word alignment matrix using latex, output statistics about them 

   helper module mt/wa2latex_helper.py

 - mt/featureModifier.py

   modify features for rules in a Moses phrase table

 - parse tree binarization for MT (method 1):
	
	- mt/berkeleyparsed2mosesxml.perl  (from moses) 
		
		convert berkeley parsed trees into moses' xml format trees

	- mt/koala-relax-parse  (from moses)

		binarize trees in moses' xml format 
		
		(binarize options: --LeftBinarize, --RightBinarize, --SAMT 1-4)

	- mt/mosesxml2berkeleyparsed.py 

		convert moses' binarized xml format trees into berkeley format trees 
		
		(only works on left or right binarized trees, doesn't work on SAMTed trees)
		
	``` bash	
	$ echo "( (S (NN I) (NN you) (NN he) (NN she)))" | berkeleyparsed2mosesxml.perl | koala-relax-parse --RightBinarize | mosesxml2berkeleyparsed.py 

	(S (TOP (NN I) (^S (NN you) (^S (NN he) (NN she)))))
	```

 - parse tree binarization for MT (method 2):

	 - mt/treeBinarizer.py

		a rule-based parse tree binarizer

 - flatten parse trees for MT:

	- mt/flattenTree.py

	  syntax: cat filename | flattenTree.py level

	  filename is a file of parse trees, one tree per line; level is how much to flatten the trees (level >= 4)

