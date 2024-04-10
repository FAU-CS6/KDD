.PHONY: all clean FORCE

TEX_FILES := $(wildcard *.tex)

all: clean $(TEX_FILES)

clean:
	rm -rf output

$(TEX_FILES): FORCE
	mkdir -p output
	python3 create_submission_pdfs.py -o output $@

FORCE: ;
