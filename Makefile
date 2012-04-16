all:
	cd /tmp
	rm -rf /tmp/move
	mkdir -p /tmp/move
	cd /tmp/move; git clone git://github.com/futuregrid/rain-move.git
	cd /tmp/move/doc/doc; ls; make html
	cp -r /tmp/move/doc/doc/build/html/* .
	git add .
	git commit -a -m "updating the github pages"
#	git commit -a _sources
#	git commit -a _static
	git push
	git checkout master
