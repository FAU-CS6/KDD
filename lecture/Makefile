################################################################################
# Settings
################################################################################

COMPILER := pdflatex
BIBTEXER := biber

SLIDES     = slides
HANDOUT    = handout
REFERENCES = body/references.bib
#FONTS      = Myriad Minion

PDFDEP := $(wildcard head/*.tex) \
          $(wildcard body/*.tex) \
          $(wildcard figures/*.tex)


################################################################################
# Variables
################################################################################

TEXINPUTS := ./themefau/:$(TEXINPUTS)
COMPILER  := TEXINPUTS=$(TEXINPUTS) $(COMPILER)

ifdef FONTS
  TEXMFLOCAL := $(shell kpsewhich -var-value TEXMFLOCAL)
endif

ifndef VERBOSE
  PIPE     := 1>/dev/null 2>/dev/null
  INDENT   := 2>&1 | sed 's/^/    /'
  COMPILER := $(COMPILER) -interaction=nonstopmode
endif

ifdef REFERENCES
  BIBDEP := $$@.bbl
endif


################################################################################
# Functions
################################################################################

check_error = \
  if [ ! $(1) -eq 0 ]; then \
    cat $(2).log | \
      perl -0777 -ne 'print m/\n! .*?\nl\.\d.*?\n.*?(?=\n)/gs' $(INDENT); \
    exit 1; \
  fi

compile = $(COMPILER) -shell-escape $(1).tex $(PIPE) || \
            $(call check_error, $$?, $(1))


################################################################################
# Targets
################################################################################

.PHONY: all %-status $(SLIDES) $(HANDOUT) clean distclean
.PRECIOUS: %.pdf %.bcf %.bbl
.SECONDEXPANSION:

all: $(SLIDES)

%-status:
	@echo "Building $*.pdf"

# .tex -> .pdf and .bcf
%.pdf %.bcf: %.tex $(PDFDEP) | $$*-status
	@# Initial compile
	@echo "  Compiling $*.tex"
	@$(call compile, $*)

# .bcf -> .bbl
%.bbl: %.bcf $(REFERENCES) | $$*-status
	@# Bibliography
	@echo "  Running $(BIBTEXER)"
	-@$(BIBTEXER) $* $(PIPE)
	@# Update references
	@echo "  Updating references"
	@$(call compile, $*)
	@# Reset time stamp of .bbl to newer than .bcf
	@touch $@

$(SLIDES) $(HANDOUT): $$@.pdf $(BIBDEP)
	@# Fill in missing references
	@if test -e $@.log \
	      && ( grep -q "There were undefined references." $@.log \
	        || grep -q "Rerun to get outlines right" $@.log ); then  \
	  echo "  Filling in missing references"; \
	  $(call compile, $@); \
	fi
	@# Fix cross-references
	@while test -e $@.log \
	      && grep -q "Rerun to get cross-references right." $@.log; do \
	  echo "  Fixing cross-references"; \
	  $(call compile, $@); \
	done

ifdef FONTS
fontinstall:
	@for f in $(FONTS); do \
	  echo "Installing font $$f to $(TEXMFLOCAL)"; \
	  sudo cp -r fonts/$$f/* $(TEXMFLOCAL) $(PIPE); \
	  if [ ! $$? -eq 0 ]; then exit 1; fi; \
	done
	@sudo $$(which mktexlsr)
	@for f in $(FONTS); do \
	  echo "Enabling font $$f"; \
	  updmap -user --disable $$f.map $(PIPE); \
	  updmap -user --enable Map=$$f.map $(PIPE); \
	  if [ ! $$? -eq 0 ]; then exit 1; fi; \
  done
endif

clean:
	rm -rf *.aux *.auxlock *.ind *.idx *.toc *.out *.log *.lot *.ilg *.dvi *.bbl \
	  *.blg *.sub *.suc *.syc *.sym *.syg *.syi *.synctex *.slg *.lol *.lof \
	  *.ist *.gls *.glo *.gli *.glg *.alg *.acr *.acn *.ps *.defn *.nlo *.satz \
	  *.nav *.snm *.xml *.synctex.gz *.synctex *.vrb *.bcf *.makefile *.figlist \
	  $$(ls figures/$(SLIDES)-figure[0-9]*.* 2>/dev/null | grep -v pdf) \
	  $$(ls figures/$(HANDOUT)-figure[0-9]*.* 2>/dev/null | grep -v pdf)

distclean: clean
	rm -f *.pdf figures/$(SLIDES)-figure[0-9]*.* figures/$(HANDOUT)-figure[0-9]*.*

