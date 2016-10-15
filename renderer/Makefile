.phony: clean

renderer.js: renderer.cpp
	em++ renderer.cpp -o renderer.js -s EXPORTED_FUNCTIONS="['_getChannels','setXShift']" 

clean:
	rm -f renderer.js
