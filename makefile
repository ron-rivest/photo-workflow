all	: pdf html tex

tex	: photoflow.text
	pandoc -f markdown -t latex -s photoflow.text -o photoflow.tex -N --toc

pdf	: photoflow.text
	pandoc -f markdown -t latex -s photoflow.text -o photoflow.pdf -N --toc

html	: photoflow.text
	pandoc -f markdown -t html -s photoflow.text -o photoflow.html -N --toc


