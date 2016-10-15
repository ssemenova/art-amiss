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
                ctx = canvas.getContext("2d");

            var imgData = ctx.createImageData(cols, rows);

            var rgb = getChannels();

            for (var i = 0; i < rgb.red.length; i++) {
                        imgData.data[i*4+0]=rgb.red[i];
                        imgData.data[i*4+1]=rgb.green[i];
                        imgData.data[i*4+2]=rgb.blue[i];
                        imgData.data[i*4+3]=255;
            }
            ctx.putImageData(imgData,0,0);
        },
        ready: function() {
            this.drawCanvas();
        }
    },
    watch: {
        binArray: function(val) {
            this.drawCanvas();
        }
    }
})

app.ready();
