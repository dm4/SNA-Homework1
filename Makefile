run:
	[ ! -d output ] && mkdir output
	./cycle.py

draw:
	[ ! -d image ] && mkdir image
	./draw.py
