VERSION = `python -c "import futuregrid_move; print futuregrid_move.RELEASE"`

all:
	make clean
	cd /tmp
	rm -rf /tmp/vc
	mkdir -p /tmp/vc
	cd /tmp/vc; git clone git://github.com/futuregrid/rain-move.git
	cd /tmp/vc/rain-move/doc; ls; make website
	cp -r /tmp/vc/rain-move/doc/build/web-${VERSION}/* .
	find . -name "*.pyc" -exec rm {} \;
	git add .
	git reset -- doc
	git reset -- src
	git reset -- .project .pydevproject .settings
	git commit -a -m "updating the github pages"
	git commit -a _sources
	git commit -a _static
	git push
	git checkout master
	rm -rf /tmp/vc
all-devmode:
	make clean
	cd /tmp
	rm -rf /tmp/vc
	mkdir -p /tmp/vc
	cd /tmp/vc; git clone git://github.com/futuregrid/rain-move.git
	git checkout master
	cd /tmp/vc/rain-move/doc; ls; make website
	git checkout gh-pages
	cp -r /tmp/vc/rain-move/doc/build/web-${VERSION}/* .
	find . -name "*.pyc" -exec rm {} \;
	git add .
	git reset -- doc
	git reset -- src
	git reset -- .project .pydevproject .settings
	git commit -a -m "updating the github pages"
	git push
	git checkout master
	rm -rf /tmp/vc
clean:
	find . -name "*~" -exec rm {} \;  
	find . -name "*.pyc" -exec rm {} \;  
	rm -rf build dist *.egg-info *~ #*
	rm -f distribute*.gz distribute*.egg 
