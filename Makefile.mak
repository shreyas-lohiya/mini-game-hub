TEX=report
LATEX=pdflatex
.PHONY: all clean

all: $(TEX).pdf

$(TEX).pdf: $(TEX).tex
	$(LATEX) $(FLAGS) $(TEX).tex
	$(LATEX) $(FLAGS) $(TEX).tex

clean:
	rm -f $(TEX).aux $(TEX).log $(TEX).out $(TEX).toc $(TEX).fls $(TEX).fdb_latexmk