all: install

sums:
	$(shell sha256sum bin/qe* > bin/sha256sums)

clean: 
	rm -rf build dist src/__pycache__ *.spec docs/_build

install:
	mkdir -p ${DESTDIR}${PREFIX}/usr/bin
	mkdir -p ${DESTDIR}${PREFIX}/usr/share/doc
	install -Dm755 src/qe.py "${DESTDIR}${PREFIX}/usr/bin/qe"
	install -Dm644 README.rst "${DESTDIR}${PREFIX}/usr/share/doc/qe"

uninstall: 
	rm -f "${DESTDIR}${PREFIX}/usr/bin/qe"
	rm -f "${DESTDIR}${PREFIX}/usr/share/doc/qe"
