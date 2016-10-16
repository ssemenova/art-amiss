_getChannels = Module.cwrap('getChannels', 'void', ['number', 'number', 'number']);

setXShift = Module.cwrap("setXShift", 'void', ['number', 'number']);
setYShift = Module.cwrap("setYShift", 'void', ['number', 'number']);

const sz = 520 * 504 * 8;
let rred = Module._malloc(sz);
let rgreen = Module._malloc(sz);
let rblue = Module._malloc(sz);

function getChannels() {
    _getChannels(rred, rgreen, rblue);

    const red = new Int32Array(Module.HEAPU8.buffer, rred, sz/8);
    const green = new Int32Array(Module.HEAPU8.buffer, rgreen, sz/8);
    const blue = new Int32Array(Module.HEAPU8.buffer, rblue, sz/8);

    return {red, green, blue};
}

setXShift(3, 10);
