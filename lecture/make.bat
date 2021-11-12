set TEXINPUTS=.\themefau

pdflatex -shell-escape presentation.tex
biber presentation
pdflatex -shell-escape presentation.tex

del *.aux *.bbl *.bcf *.blg *.nav *.out *.snm *.log *.toc *.vrb
exit
