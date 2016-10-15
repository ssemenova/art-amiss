var app = new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue.js!',
        curves: ["bla!", "bla2", "bla3"],
        attributes: [{
                name:"x-shift",
                value: 50
            },
            {
                name: "y-shift",
                value: 50
            },
            {
                name: "rotation",
                value: 50
            },
            {
                name: "x-stretch",
                value: 50
            },
            {
                name: "y-stretch",
                value: 50
            }],
        binArray: []
    },
    methods: {
        drawCanvas: function() {
            var rows = 520, //height
                cols = 504, //width
                canvas = document.getElementById("myCanvas"),
                dataSplit = reshape(this.binArray, rows, cols),
                ctx = canvas.getContext("2d");

            var imgData = ctx.createImageData(cols, rows);

            for (var i = 0; i < dataSplit.length; i+=4) {
                for (var j = 0; j < dataSplit[i].length; j++) {
                    if (dataSplit[i][j] == 0) {
                        imgData.data[i+0]=255;
                        imgData.data[i+1]=255;
                        imgData.data[i+2]=255;
                        imgData.data[i+3]=255;
                    } else {
                        imgData.data[i+0]=0;
                        imgData.data[i+1]=0;
                        imgData.data[i+2]=0;
                        imgData.data[i+3]=255;
                    }
                }
            }
            ctx.putImageData(imgData,10,10);
        },
        ready: function() {
            var xhr;
            if (window.XMLHttpRequest) {
                xhr = new XMLHttpRequest();
            } else if (window.ActiveXObject) {
                xhr = new ActiveXObject("Microsoft.XMLHTTP");
            }

            xhr.onreadystatechange = () => {
                this.binArray = xhr.responseText.split(",");
            };
            xhr.open("GET","../renderer/data");
            xhr.send();
        }
    },
    watch: {
        binArray: function(val) {
            this.drawCanvas();
        }
    }
})

app.ready();

function reshape(array, rows, cols) {
    var copy = array.slice(); // Copy all elements.

    for (var r = 0; r < rows; r++) {
        var row = [];
        for (var c = 0; c < cols; c++) {
            var i = r * cols + c;
            if (i < copy.length) {
                row.push(copy[i]);
            }
        }
        copy.push(row);
    }
    return array;
};
