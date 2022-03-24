.PHONY: all clean students solutions

ipynbfiles := $(wildcard *.ipynb)
ipynbstudents := $(patsubst %.ipynb, %-student, $(ipynbfiles))
ipynbsolutions := $(patsubst %.ipynb, %-solution, $(ipynbfiles))

all: clean students solutions

clean:
	rm -rf output

%-student: %.ipynb FORCE
	mkdir -p output
	jupyter nbconvert $< --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags={\"solution\"} --to notebook --output output/$@
	
%-solution: %.ipynb FORCE
	mkdir -p output
	jupyter nbconvert $< --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags={\"student\"} --to notebook --output output/$@

students: $(ipynbstudents)

solutions: $(ipynbsolutions)

FORCE: ;

