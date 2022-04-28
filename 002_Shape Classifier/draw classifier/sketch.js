// Shape Classifier 
// CodeSpace
// https://youtu.be/jVh6wYhJEr8

// Generate Dataset: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/dataset/sketch.js
// Training: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/training/sketch.js
// Draw Classifier: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/draw%20classifier/sketch.js

var shapeClassifier,
    canvas,
    divResult,
    inputImage,
    buttonClear;

function setup(){
    canvas = createCanvas(400, 400);
    pixelDensity(1);

    var options = {
        task: 'imageClassification'
    };

    shapeClassifier = ml5.neuralNetwork(options);

    const modelDetails = {
        model: '../training/model/model.json',
        metadata: '../training/model/model_meta.json',
        weights: '../training/model/model.weights.bin'
    };

    shapeClassifier.load(modelDetails, modelLoaded);

    background(255);
    buttonClear = createButton('Clear canvas');
    buttonClear.mousePressed(function(){
        background(255);
    });

    divResult = createDiv('Loading model...');
    inputImage = createGraphics(64, 64);
}

function modelLoaded(){
    console.log('Model is ready!');
    classifyImage();
}

function classifyImage(){
    inputImage.copy(canvas, 0, 0, 400, 400, 0, 0, 64, 64);

    shapeClassifier.classify({ image: inputImage }, getResults);
}

function getResults(error, results){
    if(error){
        console.error(error);
        return;
    }

    var label = results[0].label,
        confidence = nf(100 * results[0].confidence, 2, 1);
    
    divResult.html(`${label} ${confidence}%`);
    classifyImage();
}

function draw(){
    if(mouseIsPressed){
        strokeWeight(8);
        line(mouseX, mouseY, pmouseX, pmouseY);
    }
}
