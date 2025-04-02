const express = require("express");
const cors = require("cors");
const sqlite3 = require("sqlite3").verbose();
const bodyParser = require("body-parser");
const ExcelJS = require("exceljs");
const fs = require("fs");
const { jsPDF } = require("jspdf");
const path = require("path");

const app = express();
const PORT = 5000;

// Enable CORS for frontend running on http://127.0.0.1:5500
app.use(cors({ origin: "http://127.0.0.1:5500" }));
app.use(bodyParser.json());

// Connect to SQLite database
const db = new sqlite3.Database("./incidents.db", (err) => {
    if (err) {
        console.error("Error opening database:", err.message);
    } else {
        console.log("Connected to SQLite database.");
        db.run(
            `CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                serial TEXT,
                incidentInfo TEXT,
                injury_classification TEXT,
                casualties INTEGER,
                damage_categorization TEXT,
                nature_of_incident TEXT
            )`
        );
    }
});

// API to submit a new incident report
app.post("/report", (req, res) => {
    const {
        date,
        serial,
        incidentInfo,
        injury_classification,
        casualties,
        damage_categorization,
        nature_of_incident,
    } = req.body;

    const sql = `INSERT INTO incidents 
                 (date, serial, incidentInfo, injury_classification, casualties, damage_categorization, nature_of_incident) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)`;

    db.run(
        sql,
        [date, serial, incidentInfo, injury_classification, casualties, damage_categorization, nature_of_incident],
        function (err) {
            if (err) {
                console.error("Error inserting data:", err.message);
                return res.status(500).send("Error saving report.");
            }
            res.send({ message: "Report saved successfully!", id: this.lastID });
        }
    );
});

// API to fetch all incident reports
app.get("/incidents", (req, res) => {
    db.all("SELECT * FROM incidents", [], (err, rows) => {
        if (err) {
            console.error("Error fetching incidents:", err.message);
            res.status(500).send("Error retrieving reports.");
        } else {
            res.json(rows);
        }
    });
});

// API to generate a PDF and open it in a browser
app.get("/generate-pdf", (req, res) => {
    db.get("SELECT * FROM incidents ORDER BY id DESC LIMIT 1", [], (err, incident) => {
        if (err || !incident) {
            console.error("Error fetching the latest incident:", err ? err.message : "No incidents found.");
            return res.status(500).send("No incident reports found.");
        }

        const doc = new jsPDF();
        doc.setFont("helvetica", "bold");
        doc.setFontSize(16);
        doc.text("Incident Report", 105, 20, null, null, "center");

        doc.setFont("helvetica", "normal");
        doc.setFontSize(12);
        
        let content = `
Incident Report - Official Debrief

Date of Incident: ${incident.date}  
Incident Serial Number: ${incident.serial}  

Nature of Incident: ${incident.nature_of_incident}  

Summary:  
On ${incident.date}, an incident occurred involving ${incident.nature_of_incident}. The event has been assigned the serial number ${incident.serial}. The nature of the incident involved the following details:  

"${incident.incidentInfo}"  

Casualties & Injuries:  
The incident resulted in ${incident.casualties} casualties. The injury classification for this incident has been recorded as: "${incident.injury_classification}".  

Damage Assessment:  
The damage sustained has been categorized under damage classification: "${incident.damage_categorization}".  

Conclusion & Further Action:  
This report is generated for documentation and further analysis. Any necessary follow-up actions will be coordinated in accordance with standard operating procedures (SOPs) and relevant guidelines.
`;
        doc.text(content, 20, 40, { maxWidth: 170 });

        const pdfPath = path.join(__dirname, "incident_report.pdf");
        doc.save(pdfPath);

        // Send the file to be viewed in the browser
        res.setHeader("Content-Type", "application/pdf");
        res.setHeader("Content-Disposition", "inline; filename=incident_report.pdf");
        fs.createReadStream(pdfPath).pipe(res);
    });
});

// API to export incidents as an Excel file
app.get("/export-excel", (req, res) => {
    db.all("SELECT * FROM incidents", [], async (err, incidents) => {
        if (err) {
            console.error("Error fetching incidents:", err.message);
            return res.status(500).send("Error generating Excel.");
        }

        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet("Incident Reports");

        worksheet.columns = [
            { header: "Date", key: "date", width: 15 },
            { header: "Serial", key: "serial", width: 15 },
            { header: "Incident Info", key: "incidentInfo", width: 30 },
            { header: "Injury Classification", key: "injury_classification", width: 20 },
            { header: "Casualties", key: "casualties", width: 10 },
            { header: "Damage Categorization", key: "damage_categorization", width: 15 },
            { header: "Nature of Incident", key: "nature_of_incident", width: 20 },
        ];

        incidents.forEach((incident) => {
            worksheet.addRow(incident);
        });

        const excelPath = path.join(__dirname, "incident_reports.xlsx");
        await workbook.xlsx.writeFile(excelPath);

        res.setHeader("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        res.setHeader("Content-Disposition", "attachment; filename=incident_reports.xlsx");
        fs.createReadStream(excelPath).pipe(res);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
