new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue.js!',
        curves: ["bla!", "bla2", "bla3"],
        attributes: ["x-shift", "y-shift", "rotation", "x-stretch", "y-stretch"]
    },
    methods: {
        readFile: function() {
            var reader = require("fs");
            reader.readFile("../renderer/data", function(text){
                var textByLine = text.split(",")
            });
            console.log(textByLine);
        }
    }
})
