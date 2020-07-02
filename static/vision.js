const Y_AXIS = 1;
const X_AXIS = 2;
var background_colours = ['red', 'teal', 'darkgreen', 'mediumorchid', 'orange', 'deeppink', 'cyan', 'steelblue', 'indigo', 'darkslategray', 'mediumseagreen', 'yellow']
let yoff = 0.0; // 
let background_main, b2;
let amt, startColour, newColour;
let mode_colours_1, mode_colours_2;


function setup() {
    if (/Android|webOS|iPhone/i.test(navigator.userAgent)) {
        var canvasW = 375;
        var canvasH = 800;
        console.log("in")
    } else {
        var canvasW = 960;
        var canvasH = 360;
        console.log("in")
    }
    if (mode === 1) {
        mode_colours_1 = randomColor({
            count: 10,
            hue: 'orange',
            luminosity: 'light',
            format: 'rgb'
        });
        mode_colours_2 = randomColor({
            count: 10,
            hue: 'yellow',
            luminosity: 'light',
            format: 'rgb'
        });
    } else {
        mode_colours_1 = randomColor({
            count: 10,
            hue: 'purple',
            luminosity: 'light',
            format: 'rgb'
        });
        mode_colours_2 = randomColor({
            count: 10,
            hue: 'red',
            luminosity: 'dark',
            format: 'rgb'
        });
    }
    console.log(mode_colours_1);
    startColor = color(mode_colours_1[Math.floor(Math.random() * mode_colours_1.length)]);
    newColor = color(mode_colours_1[Math.floor(Math.random() * mode_colours_1.length)]);

    amt = 0;
    var canvas = createCanvas(canvasW, canvasH);
    var x = (windowWidth - width) / 2;
    var y = (windowHeight - height / 3) / 2;
    background_main = color(background_colours[music_key]);
    b2 = color(200);

    canvas.parent("canvasHolder");
    //canvas.position(x, y);
    generate_background(canvas);
}

function generate_background(canvas) {
    setGradient(0, 0, width, height + height / 3, background_main, b2, Y_AXIS);
}

function setGradient(x, y, w, h, c1, c2, axis) {
    noFill();

    if (axis === Y_AXIS) {
        // Top to bottom gradient
        for (let i = y; i <= y + h; i++) {
            let inter = map(i, y, y + h, 0, 1);
            let c = lerpColor(c1, c2, inter);
            stroke(c);
            line(x, i, x + w, i);
        }
    } else if (axis === X_AXIS) {
        // Left to right gradient
        for (let i = x; i <= x + w; i++) {
            let inter = map(i, x, x + w, 0, 1);
            let c = lerpColor(c1, c2, inter);
            stroke(c);
            line(i, y, i, y + h);
        }
    }
}

function draw() {
    fill(lerpColor(startColor, newColor, amt));
    amt += 0.005;
    if (amt >= 1) {
        amt = 0.0;
        startColor = newColor;
        let ran = random(1);
        console.log(ran);
        if (ran > 0.5){
            newColor = color(mode_colours_1[Math.floor(Math.random() * mode_colours_1.length)]);
        } else {
            newColor = color(mode_colours_2[Math.floor(Math.random() * mode_colours_2.length)]);
        }

    }
    beginShape();
    let xoff = 0;
    var dance_value = 0.6 * Math.log(Math.pow(dance, -1.8)) + 0.4;
    console.log(dance_value)
    var bpm_value = (0.014798 * Math.log(bpm)) - 0.060844;

    // Iterate over horizontal pixels
    for (let x = 0; x <= width; x += Math.pow(energy, -2.5)) {
        // Calculate a y value according to noise, map to

        let y = map(noise(xoff, yoff), 0, dance_value, 200, 300);

        // Set the vertex
        vertex(x, y);
        // Increment x dimension for noise
        xoff += 0.05 // wave spikey
    }
    // increment y dimension for noise
    yoff += bpm_value //speed
    vertex(width, height);
    vertex(0, height);
    endShape(CLOSE);
}