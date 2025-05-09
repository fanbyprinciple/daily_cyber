// content.js

// --- Configuration ---
const WORD_COUNT_THRESHOLDS = {
    GREEN: 50,  // 0-50 words
    YELLOW: 200 // 51-200 words
    // More than 200 words will be RED
};

const COLORS = {
    GREEN: 'rgba(200, 255, 200, 0.4)', // Light green with some transparency
    YELLOW: 'rgba(248, 248, 24, 0.4)', // Light yellow with some transparency
    RED: 'rgba(233, 54, 54, 0.4)'     // Light red with some transparency
};

// --- Selectors ---
// Primary selector for identifying email rows. Relies on ARIA roles for better stability.
const EMAIL_ROW_SELECTOR = 'table[role="grid"] tr[role="row"]';
// Selectors for subject and snippet. These are still class-based and might need future updates.
const EMAIL_SUBJECT_SELECTOR = 'span.bog'; // Often contains the subject text
const EMAIL_SNIPPET_SELECTOR = 'span.y2';   // Often contains the email snippet
// Selector for the container of email rows (specifically the tbody).
const EMAIL_LIST_TBODY_SELECTOR = 'table[role="grid"] > tbody';

// --- Helper Functions ---

/**
 * Counts the words in a given text string.
 * @param {string} text The text to count words from.
 * @returns {number} The number of words.
 */
function countWords(text) {
    if (!text || typeof text !== 'string') {
        return 0;
    }
    // Splits by whitespace and filters out empty strings that can result from multiple spaces.
    return text.trim().split(/\s+/).filter(Boolean).length;
}

/**
 * Extracts the preview text (subject + snippet) from an email row element.
 * @param {HTMLElement} emailRowElement The <tr> element representing an email.
 * @returns {string} The combined preview text.
 */
function getPreviewText(emailRowElement) {
    let subjectText = '';
    let snippetText = '';

    // Attempt to find the subject element within the row.
    const subjectElement = emailRowElement.querySelector(EMAIL_SUBJECT_SELECTOR);
    if (subjectElement) {
        subjectText = subjectElement.textContent || '';
    }

    // Attempt to find the snippet element within the row.
    const snippetElement = emailRowElement.querySelector(EMAIL_SNIPPET_SELECTOR);
    if (snippetElement) {
        snippetText = snippetElement.textContent || '';
    }

    // Combine subject and snippet for the full preview text.
    return (subjectText + ' ' + snippetText).trim();
}

/**
 * Applies the appropriate background color to an email row based on its word count.
 * @param {HTMLElement} emailRowElement The <tr> element representing an email.
 */
function colorCodeEmailRow(emailRowElement) {
    // Basic validation: ensure it's an element and not already processed.
    // Also, check if it has a reasonable number of cells (td elements) to qualify as an email row.
    // This helps filter out other `tr[role="row"]` elements that might not be actual emails (e.g., headers if any).
    if (!emailRowElement ||
        typeof emailRowElement.matches !== 'function' || // Ensure it's a valid element
        emailRowElement.dataset.colorCoded ||
        emailRowElement.querySelectorAll('td[role="gridcell"]').length < 3) { // Heuristic: email rows usually have several cells
        return;
    }

    try {
        const previewText = getPreviewText(emailRowElement);
        const wordCount = countWords(previewText);

        let color = '';
        if (wordCount <= WORD_COUNT_THRESHOLDS.GREEN) {
            color = COLORS.GREEN;
        } else if (wordCount <= WORD_COUNT_THRESHOLDS.YELLOW) {
            color = COLORS.YELLOW;
        } else {
            color = COLORS.RED;
        }

        if (color) {
            console.log(`Gmail Colorizer: Applying color ${color} to email row with word count ${wordCount}:`, emailRowElement);
            emailRowElement.style.backgroundColor = color;
            emailRowElement.dataset.colorCoded = 'true'; // Mark as processed to avoid re-coloring
        }
    } catch (error) {
        console.warn('Gmail Colorizer: Error processing row:', emailRowElement, error);
    }
}

/**
 * Processes all email rows currently matching the selector in the DOM.
 */
function processAllMatchingEmails() {
    const emailRows = document.querySelectorAll(EMAIL_ROW_SELECTOR);
    emailRows.forEach(row => {
        // Ensure the row is visible before processing.
        if (row.offsetParent !== null) {
            colorCodeEmailRow(row);
        }
    });
}

// --- Main Logic & Mutation Observer ---

console.log('Gmail Colorizer: Content script loaded. Initializing...');

// Initial processing of emails when the page loads/script runs.
// Using a small delay to give Gmail more time to fully render its initial view.
setTimeout(processAllMatchingEmails, 1000);


// Observe DOM changes to apply coloring to newly loaded emails.
const observerCallback = (mutationsList, observer) => {
    for (const mutation of mutationsList) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            mutation.addedNodes.forEach(node => {
                // Check if the added node is an element node.
                if (node.nodeType === Node.ELEMENT_NODE) {
                    // If the added node itself is an email row:
                    if (node.matches(EMAIL_ROW_SELECTOR)) {
                        if (node.offsetParent !== null) { // Check visibility
                            colorCodeEmailRow(node);
                        }
                    }
                    // If the added node contains email rows (e.g., a batch of rows loaded):
                    else {
                        const newRows = node.querySelectorAll(EMAIL_ROW_SELECTOR);
                        newRows.forEach(row => {
                            if (row.offsetParent !== null) { // Check visibility
                                colorCodeEmailRow(row);
                            }
                        });
                    }
                }
            });
        }
        // Handle attribute changes on existing rows (e.g., read/unread status might change appearance or classes).
        // This can help if Gmail reuses row elements but changes attributes.
        else if (mutation.type === 'attributes' && mutation.target.nodeType === Node.ELEMENT_NODE && mutation.target.matches(EMAIL_ROW_SELECTOR)) {
            if (mutation.target.offsetParent !== null) { // Check visibility
                // Reset 'colorCoded' status and reprocess, as attributes might affect content/appearance.
                delete mutation.target.dataset.colorCoded;
                colorCodeEmailRow(mutation.target);
            }
        }
    }
};

// Attempt to find the target node (tbody of the email list) to observe.
// Using a function to allow retrying if not immediately available.
function startObserver() {
    const targetNode = document.querySelector(EMAIL_LIST_TBODY_SELECTOR);

    if (targetNode) {
        const observer = new MutationObserver(observerCallback);
        // Configure observer: watch for new child elements and attribute changes within the subtree.
        const config = {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['class', 'style'] // Observe specific attributes that might change
        };
        observer.observe(targetNode, config);
        console.log('Gmail Colorizer: MutationObserver started on:', targetNode);

        // Optional: Disconnect observer on page unload.
        window.addEventListener('unload', () => {
            observer.disconnect();
            console.log('Gmail Colorizer: MutationObserver disconnected.');
        });
        return true; // Observer started
    }
    return false; // Target node not found
}

// Try to start the observer. If Gmail loads elements dynamically,
// the target might not be present immediately. Retry a few times.
let observerStarted = false;
let retries = 5;
const retryInterval = setInterval(() => {
    observerStarted = startObserver();
    if (observerStarted || retries <= 0) {
        clearInterval(retryInterval);
        if (!observerStarted) {
            console.warn('Gmail Colorizer: Email list tbody container not found after multiple retries. Falling back to observing document.body. This is less efficient and might not work as well.');
            // Fallback: Observe the entire document body if the specific tbody isn't found.
            // This is less efficient and more prone to processing unrelated changes.
            const bodyObserver = new MutationObserver(observerCallback);
            bodyObserver.observe(document.body, { childList: true, subtree: true });
            window.addEventListener('unload', () => {
                bodyObserver.disconnect();
                console.log('Gmail Colorizer: Fallback MutationObserver on document.body disconnected.');
            });
        }
    }
    retries--;
}, 2000); // Retry every 2 seconds

// A periodic re-scan can catch emails missed by the observer, especially if Gmail does tricky DOM manipulations.
// However, rely more on the MutationObserver for efficiency.
// setInterval(processAllMatchingEmails, 7000); // e.g., every 7 seconds. Use with caution for performance.

console.log('Gmail Colorizer: Initialization sequence started.');
