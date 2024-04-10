.PHONY: all clean students solutions FORCE

TEX_FILES := $(wildcard *.tex)

STUDENT_TARGETS := $(TEX_FILES:.tex=-Student)
SOLUTION_TARGETS := $(TEX_FILES:.tex=-Solution)

all: clean students solutions

clean:
	rm -rf output

students: $(STUDENT_TARGETS)

solutions: $(SOLUTION_TARGETS)

%-Student: %.tex FORCE
	mkdir -p output
	python3 create_exercise_archive.py -o output -s student $<

%-Solution: %.tex FORCE
	mkdir -p output
	python3 create_exercise_archive.py -o output -s solution $<

FORCE: ;
