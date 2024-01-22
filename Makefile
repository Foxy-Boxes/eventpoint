INPUT?=example

all:
	python3 parse.py $(INPUT) ; \
	g++ -O3 tick.cpp -o main
