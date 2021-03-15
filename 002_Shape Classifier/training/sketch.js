// Shape Classifier 
// CodeSpace

// Generate Dataset: 
// Training: 
// Draw Classifier:

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
