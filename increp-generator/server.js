const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
const bodyParser = require("body-parser");
const fs = require("fs");
const ExcelJS = require("exceljs");
const PDFDocument = require("pdfkit");

const app = express();
const PORT = 5000;

// At the top of your server file, after requiring express
app.use(cors({
    origin: 'http://localhost', // Or your specific frontend URL
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type', 'Accept']
}));
app.use(bodyParser.json());

// ✅ Initialize SQLite Database
const db = new sqlite3.Database("./incidents.db", sqlite3.OPEN_READWRITE | sqlite3.OPEN_CREATE, (err) => {
    if (err) {
        console.error("Error connecting to SQLite database:", err.message);
    } else {
        console.log("Connected to SQLite database.");
    }
});

// ✅ Create incidents table if not exists
db.run(`
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        serial TEXT,
        incidentInfo TEXT,
        injury_classification TEXT,
        casualties INTEGER,
        damage_categorization TEXT,
        nature_of_incident TEXT,
        department TEXT,
        cause_classification TEXT,
        reported_incident TEXT,
        previous_incident_reference TEXT,
        incident_assistance TEXT
    )
`);

// ✅ API to store incident report
app.post("/report", (req, res) => {
    const {
        date, serial, incidentInfo, injury_classification,
        casualties, damage_categorization, nature_of_incident,
        department, cause_classification, reported_incident,
        previous_incident_reference, incident_assistance
    } = req.body;

    const query = `
        INSERT INTO incidents 
        (date, serial, incidentInfo, injury_classification, casualties, damage_categorization, nature_of_incident, department, cause_classification, reported_incident, previous_incident_reference, incident_assistance) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

    db.run(query, [date, serial, incidentInfo, injury_classification, casualties, damage_categorization, nature_of_incident, department, cause_classification, reported_incident, previous_incident_reference, incident_assistance], function (err) {
        if (err) {
            res.status(500).json({ error: err.message });
        } else {
            res.json({ message: "Incident reported successfully!", id: this.lastID });
        }
    });
});

// ✅ API to generate PDF of all incidents
app.get("/generate-pdf", (req, res) => {
    db.all("SELECT * FROM incidents", [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }

        const doc = new PDFDocument();
        const filePath = "./incident_report.pdf";

        // Create reports directory if it doesn't exist
        if (!fs.existsSync('./reports')) {
            fs.mkdirSync('./reports');
        }

        doc.pipe(fs.createWriteStream(filePath));

        doc.fontSize(18).text("Incident Report", { align: "center" });
        doc.moveDown();

        rows.forEach((incident, index) => {
            doc.fontSize(12).text(`Incident ${index + 1}`, { underline: true });
            doc.text(`Date: ${incident.date}`);
            doc.text(`Serial: ${incident.serial}`);
            doc.text(`Info: ${incident.incidentInfo}`);
            doc.text(`Injury Classification: ${incident.injury_classification}`);
            doc.text(`Casualties: ${incident.casualties}`);
            doc.text(`Damage Categorization: ${incident.damage_categorization}`);
            doc.text(`Nature of Incident: ${incident.nature_of_incident}`);
            doc.text(`Department: ${incident.department}`);
            doc.text(`Cause Classification: ${incident.cause_classification}`);
            doc.text(`Reported Incident: ${incident.reported_incident}`);
            doc.text(`Previous Incident Reference: ${incident.previous_incident_reference}`);
            doc.text(`Incident Assistance: ${incident.incident_assistance}`);
            doc.moveDown();
        });

        doc.end();

        doc.on("finish", () => {
            res.download(filePath, 'incident_report.pdf', (err) => {
                // Delete the file after sending
                if (err) {
                    console.error('Error downloading file:', err);
                }
                fs.unlink(filePath, (unlinkErr) => {
                    if (unlinkErr) console.error('Error deleting file:', unlinkErr);
                });
            });
        });
    });
});

app.get("/export-excel", async (req, res) => {
    db.all("SELECT * FROM incidents", [], async (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }

        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet("Incidents");

        // Add header row
        worksheet.addRow([
            "ID", "Date", "Serial", "Incident Info", "Injury Classification", "Casualties",
            "Damage Categorization", "Nature of Incident", "Department", "Cause Classification",
            "Reported Incident", "Previous Incident Reference", "Incident Assistance"
        ]);

        // Add data rows
        rows.forEach(row => {
            worksheet.addRow([
                row.id, row.date, row.serial, row.incidentInfo, row.injury_classification,
                row.casualties, row.damage_categorization, row.nature_of_incident,
                row.department, row.cause_classification, row.reported_incident,
                row.previous_incident_reference, row.incident_assistance
            ]);
        });

        // Write Excel file
        const filePath = "./incident_reports.xlsx";
        await workbook.xlsx.writeFile(filePath);
        
        res.download(filePath, 'incident_reports.xlsx', (err) => {
            // Delete the file after sending
            if (err) {
                console.error('Error downloading file:', err);
            }
            fs.unlink(filePath, (unlinkErr) => {
                if (unlinkErr) console.error('Error deleting file:', unlinkErr);
            });
        });
    });
});

// ✅ Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

// Add this endpoint to your server.js
app.get("/incidents", (req, res) => {
    console.log("Fetching all incidents..."); // Debug log
    db.all("SELECT * FROM incidents ORDER BY date DESC", [], (err, rows) => {
        if (err) {
            console.error("Database error:", err.message); // Debug log
            return res.status(500).json({ error: err.message });
        }
        console.log(`Found ${rows.length} incidents`); // Debug log
        res.json(rows);
    });
});
