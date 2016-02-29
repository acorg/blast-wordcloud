.PHONY: lint, pep8, pyflakes, wc, clean

lint: pep8 pyflakes

pep8:
	find . -name '*.py' -print0 | xargs -0 pep8

pyflakes:
	find .  -name '*.py' -print0 | xargs -0 pyflakes

wc:
	find . -name '*.py' -print0 | xargs -0 wc -l

clean:
	find . \( -name '*.pyc' -o -name '*~' \) -print0 | xargs -0 rm
	find . -name '__pycache__' -type d -print0 | xargs -0 rmdir
