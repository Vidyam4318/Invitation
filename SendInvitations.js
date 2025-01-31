import React, { useState } from 'react';
import axios from 'axios';
import './SendInvitations.css';

const SendInvitations = () => {
    const [files, setFiles] = useState([]);

    const handleFileChange = (event) => {
        setFiles([...event.target.files]); // Store multiple selected files
    };

    const sendInvites = async () => {
        if (files.length === 0) {
            alert('Please select at least one file to upload.');
            return;
        }

        const formData = new FormData();
        files.forEach((file) => {
            formData.append('files', file); // Append multiple files
        });

        try {
            // Upload files to the server
            const uploadResponse = await axios.post('http://localhost:5002/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            alert(uploadResponse.data.message); // Show success or failure message

            // Trigger email sending
            const emailResponse = await axios.post('http://localhost:5002/send-invites', {
                filePaths: uploadResponse.data.filePaths, // Pass multiple file paths to the backend
            });

            alert(emailResponse.data.message);
        } catch (error) {
            alert('Error: ' + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div>
            <input type="file" multiple onChange={handleFileChange} accept=".pdf, .doc, .docx" />
            <button onClick={sendInvites}>Upload and Send Invitations</button>
        </div>
    );
};

export default SendInvitations;
