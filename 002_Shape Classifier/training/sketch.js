// Shape Classifier 
// CodeSpace

// Generate Dataset: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/dataset/sketch.js
// Training: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/training/sketch.js
// Draw Classifier: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/draw%20classifier/sketch.js

var circles = [],
    squares = [],
    triangles = [];

function preload(){
    for(var i = 0; i < 100; i++){
        var index = nf(i + 1, 4, 0);
        circles[i] = loadImage(`../dataset/data/circle${index}.png`);
        squares[i] = loadImage(`../dataset/data/square${index}.png`);
        triangles[i] = loadImage(`../dataset/data/triangle${index}.png`);
    }
}

var shapeClassifier;

function setup(){
    createCanvas(400, 400);

    var options = {
        inputs: [64, 64, 4],
        task: 'imageClassification',
        debug: true
    };

    shapeClassifier = ml5.neuralNetwork(options);

    for(var i = 0; i < circles.length; i++){
        shapeClassifier.addData({ image: circles[i] }, { label: 'circle' });
        shapeClassifier.addData({ image: squares[i] }, { label: 'square' });
        shapeClassifier.addData({ image: triangles[i] }, { label: 'triangle' });
    }

    shapeClassifier.normalizeData();
    shapeClassifier.train({ epochs: 80}, finishedTraining);
}

function finishedTraining(){
    console.log('Training finished!');
    shapeClassifier.save();
}
