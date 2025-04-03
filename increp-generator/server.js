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

// Enable CORS for frontend
app.use(cors({ origin: "http://127.0.0.1:5500" }));
app.use(bodyParser.json());

// Connect to SQLite database
const db = new sqlite3.Database("./incidents.db", (err) => {
    if (err) {
        console.error("Error opening database:", err.message);
    } else {
        console.log("Connected to SQLite database.");
        db.run(`
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_field TEXT,
                to_field TEXT,
                date TEXT,
                serial TEXT,
                incidentInfo TEXT,
                priority TEXT,
                security_classification TEXT,
                injury_classification TEXT,
                casualties INTEGER,
                damage_categorization TEXT,
                cause_classification TEXT,
                nature_of_incident TEXT,
                other_info TEXT
            )
        `);
    }
});

// API to submit a new incident report
app.post("/report", (req, res) => {
    const {
        from,
        to,
        date,
        serial,
        incidentInfo,
        priority,
        security_classification,
        injury_classification,
        casualties,
        damage_categorization,
        cause_classification,
        nature_of_incident,
        other_info
    } = req.body;

    const sql = `INSERT INTO incidents 
        (from_field, to_field, date, serial, incidentInfo, priority, security_classification, injury_classification, casualties, damage_categorization, cause_classification, nature_of_incident, other_info) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;

    db.run(
        sql,
        [from, to, date, serial, incidentInfo, priority, security_classification, injury_classification, casualties, damage_categorization, cause_classification, nature_of_incident, other_info],
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

// API to generate a PDF report
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
        const generateIncidentReport = (incident) => {
            return `
                INCIDENT REPORT - OFFICIAL DEBRIEF
        
                FROM: ${incident.from_field}                            ${incident.priority}  
                TO:   ${incident.to_field}                                  ${incident.security_classification}  
        
                -------------------------------------------------------------------------------------------
        
                DATE OF INCIDENT: ${incident.date}  
                INCIDENT SERIAL NUMBER: ${incident.serial}  
        
                --------------------------------------------------------------------------------------------
        
                (A) ${incident.nature_of_incident.toUpperCase()}
        
                (B) ${incident.incidentInfo.toUpperCase()} 
        
                (C) REPORTED  ${incident.casualties.toUpperCase()} CASUALTIES. 
                    WITH INJURY CLASSIFICATION BEING ${incident.injury_classification.toUpperCase()}.
                 
                (D) THE DAMAGE IS CATEGORIZED INTO ${incident.damage_categorization.toUpperCase()}.
        
                (E) THE CAUSE IS IDENTIFIED AS ${incident.cause_classification.toUpperCase()}.
        
                (F) "${incident.other_info.toUpperCase()}"  
        
                (G) THIS REPORT IS GENERATED FOR DOCUMENTATION AND FURTHER ACTION.
            `;
        };
        let content = generateIncidentReport(incident); 
        doc.text(content, 20, 40, { maxWidth: 170 });

        const pdfPath = path.join(__dirname, "incident_report.pdf");
        doc.save(pdfPath);

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
            { header: "From", key: "from_field", width: 15 },
            { header: "To", key: "to_field", width: 15 },
            { header: "Date", key: "date", width: 15 },
            { header: "Serial", key: "serial", width: 15 },
            { header: "Incident Info", key: "incidentInfo", width: 30 },
            { header: "Priority", key: "priority", width: 15 },
            { header: "Security Classification", key: "security_classification", width: 20 },
            { header: "Injury Classification", key: "injury_classification", width: 20 },
            { header: "Casualties", key: "casualties", width: 10 },
            { header: "Damage Categorization", key: "damage_categorization", width: 20 },
            { header: "Cause Classification", key: "cause_classification", width: 20 },
            { header: "Nature of Incident", key: "nature_of_incident", width: 20 },
            { header: "Other Info", key: "other_info", width: 30 }
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
    console.log(`✅ Server is running on http://localhost:${PORT}`);
});
