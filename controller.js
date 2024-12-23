const ws281x = require('rpi-ws281x-native');

// Configuration
const LED_COUNT = 144; // Number of LEDs in your strip
const brightnessPercentage = 0.5;
const brightness = Math.round(255 * brightnessPercentage); // Brightness level (0-255)

// Initialize the LED strip
ws281x.init(LED_COUNT);
ws281x.setBrightness(brightness);

// Create a pixel buffer
const pixels = new Uint32Array(LED_COUNT);

// Helper function to create a color from RGB values
function rgbToColor(r, g, b) {
    return (r << 16) | (g << 8) | b;
}

// Color wipe effect
function colorWipe(color, wait) {
    for (let i = 0; i < LED_COUNT; i++) {
        pixels[i] = color;
        ws281x.render(pixels);
        sleep(wait);
    }
}

// Rainbow cycle effect
function rainbowCycle(wait) {
    for (let j = 0; j < 256; j++) {
        for (let i = 0; i < LED_COUNT; i++) {
            const rcIndex = (i * 256 / LED_COUNT + j) & 255;
            pixels[i] = wheel(rcIndex);
        }
        ws281x.render(pixels);
        sleep(wait);
    }
}

// Generate rainbow colors across 0-255 positions
function wheel(pos) {
    if (pos < 85) {
        return rgbToColor(255 - pos * 3, pos * 3, 0);
    } else if (pos < 170) {
        pos -= 85;
        return rgbToColor(0, 255 - pos * 3, pos * 3);
    } else {
        pos -= 170;
        return rgbToColor(pos * 3, 0, 255 - pos * 3);
    }
}

// Sleep function (synchronous delay)
function sleep(ms) {
    const end = Date.now() + ms;
    while (Date.now() < end) { }
}

// Main loop
try {
    setInterval(() => {
        colorWipe(rgbToColor(255, 100, 50), 100); // Orange
        colorWipe(rgbToColor(0, 255, 0), 100);    // Green
        colorWipe(rgbToColor(0, 0, 255), 100);    // Blue
        rainbowCycle(10);                         // Rainbow
    }, 1000);
} catch (err) {
    console.error('Error:', err);
    ws281x.reset();
}

// Reset LEDs on exit
process.on('SIGINT', () => {
    ws281x.reset();
    process.exit(0);
});
