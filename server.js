const express = require('express');
const { exec } = require('child_process');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json()); // To parse incoming JSON requests

const port = 5002;

// Configure multer for file uploads
const uploadFolder = path.join(__dirname, 'uploads');
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, uploadFolder); // Save files in the "uploads" folder
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`); // Add timestamp to avoid filename conflicts
    },
});
const upload = multer({ storage }).array('files'); // Accept multiple files

// Ensure the upload folder exists
if (!fs.existsSync(uploadFolder)) {
    fs.mkdirSync(uploadFolder);
}

// Route to upload files
app.post('/upload', upload, (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.status(400).send({ message: 'No files uploaded' });
    }
    const filePaths = req.files.map(file => file.path);
    console.log(`Files uploaded: ${filePaths}`);
    res.send({ message: 'Files uploaded successfully', filePaths });
});

// POST route to trigger the Python script and send emails
app.post('/send-invites', (req, res) => {
    const filePaths = req.body.filePaths; // Retrieve the uploaded file paths

    if (!filePaths || filePaths.length === 0) {
        return res.status(400).send({ message: 'File paths are required' });
    }

    // Convert file paths array to space-separated string for Python script
    const fileArgs = filePaths.map(path => `"${path}"`).join(' ');

    // Run the Python script and pass the file paths as arguments
    exec(`python C:\\Users\\cdac\\invitation\\python\\send_bulk_email.py ${fileArgs}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            console.error(`stderr: ${stderr}`);
            return res.status(500).send({ message: 'Error sending emails', error: stderr });
        }
        console.log(stdout);  // Log standard output
        res.send({ message: 'Emails sent successfully!' });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Backend running on http://localhost:${port}`);
});
