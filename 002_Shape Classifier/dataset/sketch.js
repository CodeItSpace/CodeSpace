// Shape Classifier 
// CodeSpace

// Generate Dataset: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/dataset/sketch.js 
// Training: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/training/sketch.js
// Draw Classifier: https://github.com/CodeItSpace/CodeSpace/blob/main/002_Shape%20Classifier/draw%20classifier/sketch.js

function setup(){
    createCanvas(64, 64);
}

function draw(){
    for(var i = 0; i < 3; i++){
        background(255);
        push();
        strokeWeight(4);
        var r = random(8, 24),
            x = random(r, width - r),
            y = random(r, height - r);
        stroke(random(100), random(100), random(100));
        translate(x, y);

        if(i == 0){
            circle(0, 0, r * 2);
            save(`circle${nf(frameCount, 4, 0)}.png`);
        }
        else if(i == 1){
            rectMode(CENTER);
            rotate(random(-0.2, 0.2));
            square(0, 0, r * 2);
            save(`square${nf(frameCount, 4, 0)}.png`);
        }
        else if(i == 2){
            rotate(random(-0.2, 0.2));
            triangle(0, -r, r, r, -r, r);
            save(`triangle${nf(frameCount, 4, 0)}.png`);
        }
        pop();
    }

    if(frameCount == 1){
        exit();
    }
}
