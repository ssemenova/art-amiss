.phony: clean

renderer.js: renderer.cpp
	em++ renderer.cpp -o renderer.js -O3 -s TOTAL_MEMORY=56777216 -s EXPORTED_FUNCTIONS="['_getChannels','_setXShift', '_setYShift']"
	mv renderer.js.mem ..

clean:
	rm -f renderer.js ../renderer.js.mem
