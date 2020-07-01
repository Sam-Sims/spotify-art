var background_colours = ['yellow', 'yellow', 'orange', 'red', 'red', 'pink', 'pink', 'purple', 'blue', 'blue', 'green', 'green'];
var currentColour = background_colours[music_key];
const Y_AXIS = 1;
const X_AXIS = 2;
let b1, b2

function setup() {
    let cnv = createCanvas(960, 360)
    var x = (windowWidth - width) / 2;
    var y = (windowHeight - height) / 2;
    cnv.position(x, y);

    console.log("mode: " + mode + ", valence: " + valence + ", energy: " + energy + ", music key: " + music_key);
    sunSize = random(75, 150);
    sunRange = random(5, 10);
    b1 = color(currentColour);
    b2 = color(255);

    setGradient(0, 0, width, height + height / 3, b1, b2, Y_AXIS);
    sun()
}

function sun() {
      sunColours = randomColor({
          hue: 'yellow',
          count: 2
        });
      var sunColor = sunColours[0];
      sunPos = [random(20, width), random(20, (height / 2) - 50)];
      fill(sunColor);
      ellipse(sunPos[0], sunPos[1], 70);
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