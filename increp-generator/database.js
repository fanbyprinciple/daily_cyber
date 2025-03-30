const sqlite3 = require("sqlite3").verbose();

// Connect to SQLite database
const db = new sqlite3.Database("./incidents.db", sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE, (err) => {
    if (err) console.error(err.message);
    else console.log("✅ Connected to SQLite database.");
});

// Create incidents table with new fields
db.run(`
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        serial TEXT NOT NULL,
        incidentInfo TEXT NOT NULL,
        category TEXT NOT NULL,
        impact TEXT NOT NULL,
        location TEXT NOT NULL,
        reporter TEXT NOT NULL,
        remediation TEXT NOT NULL,
        injury_classification TEXT NOT NULL,
        casualties INTEGER NOT NULL,
        damage_categorization TEXT NOT NULL,
        nature_of_incident TEXT NOT NULL,
        department TEXT NOT NULL,
        cause_classification TEXT NOT NULL,
        brief_description TEXT NOT NULL,
        reported_incident TEXT NOT NULL,
        previous_incident_reference TEXT,
        incident_assistance TEXT NOT NULL
    )
`);

module.exports = db;
