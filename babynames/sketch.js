let names = { male: [], female: [] };
let selectedGender = "Male";
let displayedName = "";
let nameMeaning = "";
let lengthSlider, searchInput, saveButton, generateButton, maleButton, femaleButton; // Make buttons global for styling
let savedNames = [];

// Hardcoded meanings (as in original)
const meanings = {
    "Arjun": "Bright, shining, white",
    "Lakshmi": "Goddess of wealth",
    "Vishnu": "The preserver, all-pervading",
    "Sita": "Furrow, Goddess of agriculture",
    "Shiva": "Auspicious, pure",
    "Radha": "Success, prosperity"
    // Add more meanings if available in your data source or known
};

// Data source URLs (keep as they are)
const FEMALE_NAMES_URL = "https://gist.githubusercontent.com/mbejda/9b93c7545c9dd93060bd/raw/b582593330765df3ccaae6f641f8cddc16f1e879/Indian-Female-Names.csv";
const MALE_NAMES_URL = "https://gist.githubusercontent.com/mbejda/7f86ca901fe41bc14a63/raw/38adb475c14a3f44df9999c1541f3a72f472b30d/Indian-Male-Names.csv";


function preload() {
    // Keep preload as is
    fetch(FEMALE_NAMES_URL)
        .then(response => response.text())
        .then(data => {
            names.female = data.split("\n").map(line => line.match(/^(.*?),/)).filter(match => match && match[1] && match[1].trim()).map(match => match[1].trim());
        })
        .catch(error => console.error("Error fetching female names:", error));

    fetch(MALE_NAMES_URL)
        .then(response => response.text())
        .then(data => {
            names.male = data.split("\n").map(line => line.match(/^(.*?),/)).filter(match => match && match[1] && match[1].trim()).map(match => match[1].trim());
        })
        .catch(error => console.error("Error fetching male names:", error));
}

function setup() {
    createCanvas(500, 550); // Slightly taller canvas for spacing
    background(245, 245, 245); // Lighter background
    textFont('Arial, sans-serif');

    let controlStartX = 50;
    let controlWidth = width - 2 * controlStartX;
    let currentY = 20;

    // --- Title ---
    let title = createElement("h2", "Sanskrit Name Generator");
    // Center the title using CSS within the element
    title.style("width", "100%");
    title.style("text-align", "center");
    title.position(0, currentY); // Position at top, centering handled by text-align
    title.style("color", "#2C3E50"); // Dark blue-grey
    title.style("font-family", "Arial, sans-serif");
    currentY += 60;

    // --- Gender Selection ---
    // Center the button pair
    let genderButtonWidth = 80;
    let genderButtonSpacing = 10;
    let genderStartX = (width / 2) - (genderButtonWidth + genderButtonSpacing / 2);

    maleButton = createButton("Male");
    maleButton.position(genderStartX, currentY);
    maleButton.style("width", `${genderButtonWidth}px`);
    maleButton.style("padding", "10px");
    maleButton.style("border", "none");
    maleButton.style("border-radius", "4px");
    maleButton.style("cursor", "pointer");
    maleButton.mousePressed(() => {
        selectedGender = "Male";
        updateButtonStyles();
        // Optionally regenerate name on gender change: generateName();
    });

    femaleButton = createButton("Female");
    femaleButton.position(genderStartX + genderButtonWidth + genderButtonSpacing, currentY);
    femaleButton.style("width", `${genderButtonWidth}px`);
    femaleButton.style("padding", "10px");
    femaleButton.style("border", "none");
    femaleButton.style("border-radius", "4px");
    femaleButton.style("cursor", "pointer");
    femaleButton.mousePressed(() => {
        selectedGender = "Female";
        updateButtonStyles();
        // Optionally regenerate name on gender change: generateName();
    });
    updateButtonStyles(); // Set initial styles
    currentY += 55; // Increase spacing after buttons


    // --- Length Slider ---
    let labelLength = createP('Name Length:'); // Create a label element
    labelLength.style('font-size', '14px');
    labelLength.style('color', '#555');
    labelLength.position(controlStartX, currentY - 5); // Position label slightly above
    lengthSlider = createSlider(3, 12, 5, 1); // Range 3-12, default 5, step 1
    lengthSlider.position(controlStartX, currentY + 20);
    lengthSlider.style("width", `${controlWidth}px`);
    lengthSlider.input(updateLengthDisplay); // Update display dynamically
    currentY += 60; // Space for label and slider


    // --- Search Input ---
    let labelSearch = createP('Starts with (optional):');
    labelSearch.style('font-size', '14px');
    labelSearch.style('color', '#555');
    labelSearch.position(controlStartX, currentY - 5);
    searchInput = createInput("");
    searchInput.position(controlStartX, currentY + 20);
    searchInput.style("width", `${controlWidth - 18}px`); // Account for padding
    searchInput.style("padding", "8px");
    searchInput.style("border", "1px solid #ccc");
    searchInput.style("border-radius", "4px");
    searchInput.attribute("placeholder", "e.g., A");
    searchInput.input(generateName); // Generate name on input change
    currentY += 65;


    // --- Action Buttons ---
    let actionButtonWidth = 150;
    let actionButtonSpacing = 20;
    let actionStartX = (width / 2) - (actionButtonWidth + actionButtonSpacing / 2);

    generateButton = createButton("Generate Name");
    generateButton.position(actionStartX, currentY);
    styleActionButton(generateButton, "#27AE60"); // Green
    generateButton.mousePressed(generateName);

    // saveButton = createButton("Save Name");
    // saveButton.position(actionStartX + actionButtonWidth + actionButtonSpacing, currentY);
    // styleActionButton(saveButton, "#F39C12"); // Orange
    // saveButton.mousePressed(saveName);

    // Initial length display update
    updateLengthDisplay();
}

// Helper function to style action buttons consistently
function styleActionButton(button, bgColor) {
    button.style("background-color", bgColor);
    button.style("color", "white");
    button.style("padding", "10px 15px");
    button.style("border", "none");
    button.style("border-radius", "4px");
    button.style("cursor", "pointer");
    button.style("font-size", "14px");
    // Basic hover effect
    button.mouseOver(() => button.style("filter", "brightness(1.1)"));
    button.mouseOut(() => button.style("filter", "brightness(1)"));
}


function generateName() {
    // Keep generateName as is (logic is fine)
    let currentList = names[selectedGender.toLowerCase()];
    if (!currentList || currentList.length === 0) {
        // Handle case where names haven't loaded yet or list is empty
        if (names.male.length > 0 || names.female.length > 0) { // Check if *any* names loaded
            displayedName = "No names found with criteria";
        } else {
            displayedName = "Loading names..."; // Or indicate loading/error state better
        }
        nameMeaning = "";
        return; // Exit early
    }

    let filteredNames = currentList.filter(name => {
        const nameLower = name ? name.toLowerCase() : ''; // Add check for undefined name
        const searchVal = searchInput.value().toLowerCase().trim();
        return name && // Ensure name is defined
            name.length === lengthSlider.value() &&
            (searchVal === "" || nameLower.startsWith(searchVal));
    });

    if (filteredNames.length > 0) {
        displayedName = random(filteredNames);
        fetchNameMeaning(displayedName);
    } else {
        displayedName = "No names found";
        nameMeaning = "";
    }
    updateLengthDisplay(); // Update display in case length changed
}

function fetchNameMeaning(name) {
    // Keep fetchNameMeaning as is
    nameMeaning = meanings[name] || "Meaning not available";
}

function saveName() {
    // Keep saveName as is (console log only as per user code)
    if (displayedName && displayedName !== "" && displayedName !== "No names found" && !displayedName.startsWith("Loading")) {
        if (!savedNames.includes(displayedName)) {
            savedNames.push(displayedName);
            console.log("Saved Names:", savedNames);
            // Add temporary visual feedback if desired in future
        } else {
            console.log(`"${displayedName}" is already saved.`);
            // Add temporary visual feedback if desired in future
        }
    }
}

// Function to update button visual state
function updateButtonStyles() {
    // Active/Inactive styles
    const activeMaleBg = "#3498DB"; // Blue
    const activeFemaleBg = "#E74C3C"; // Red
    const inactiveBg = "#bdc3c7"; // Grey
    const activeColor = "white";
    const inactiveColor = "#ecf0f1"; // Lighter grey text

    if (selectedGender === "Male") {
        maleButton.style("background-color", activeMaleBg);
        maleButton.style("color", activeColor);
        femaleButton.style("background-color", inactiveBg);
        femaleButton.style("color", inactiveColor);
    } else {
        femaleButton.style("background-color", activeFemaleBg);
        femaleButton.style("color", activeColor);
        maleButton.style("background-color", inactiveBg);
        maleButton.style("color", inactiveColor);
    }
}

// --- Draw function for dynamic text display ---
function draw() {
    // Only redraw background if needed, or draw specific areas
    // For simplicity, we redraw background
    background(245, 245, 245);

    let displayY = 400; // Starting Y for the results display area

    // Draw a subtle line separator
    stroke(200);
    line(50, displayY - 20, width - 50, displayY - 20);
    noStroke(); // Turn off stroke for text

    // Display the generated name
    if (displayedName) {
        fill(44, 62, 80); // Dark text color
        if (displayedName === "No names found" || displayedName.startsWith("Loading")) {
            fill(149, 165, 166); // Greyer color for status messages
            textSize(22);
        } else {
            fill(52, 73, 94); // Dark blue for name
            textSize(32);
        }
        textAlign(CENTER, CENTER);
        text(displayedName, width / 2, displayY);
    }

//     // Display the meaning
//     if (nameMeaning) {
//         fill(127, 140, 141); // Muted grey for meaning
//         textSize(16);
//         textAlign(CENTER, CENTER);
//         text(nameMeaning, width / 2, displayY + 40);
//     }

    // Display current slider value near the slider (optional, can remove if label is enough)
    fill(50);
    textSize(14);
    textAlign(LEFT, CENTER);
    text(lengthSlider.value(), 50 + (width - 2 * 50) + 10, 150 + 28); // Position next to slider
}

// Separate function to update the length display text (called by slider)
function updateLengthDisplay() {
    // This function doesn't strictly need to do anything if the value is drawn in draw()
    // But it's good practice if you wanted to update a dedicated p5 label element instead
    // For now, draw() handles showing the value next to the slider
}