.phony: clean

renderer.js: renderer.cpp
	em++ renderer.cpp -o renderer.js -s EXPORTED_FUNCTIONS="['_getChannels','_setXShift', '_setYShift']" 

clean:
	rm -f renderer.js
