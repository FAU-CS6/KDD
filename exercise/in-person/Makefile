.PHONY: all clean students solutions

folders := $(wildcard */)
foldersstudents := $(patsubst %/, %-Student, $(folders))
folderssolutions := $(patsubst %/, %-Solution, $(folders))

all: clean students solutions

clean:
	rm -rf output

%-Student: %/ FORCE
	mkdir -p output
	python3 create_exercise_archive.py -o output/$@ -s student $<

%-Solution: %/ FORCE
	mkdir -p output
	python3 create_exercise_archive.py -o output/$@ -s solution $<

students: $(foldersstudents)

solutions: $(folderssolutions)

FORCE: ;
