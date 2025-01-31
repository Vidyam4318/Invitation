import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import sys
import os
import re
import zipfile

# Replace with your details
sender_email = "v5071634@gmail.com"  # Your Gmail address
app_password = "mffn mobb mtgd vvgt"  # Replace with your generated App Password

# Load email addresses from an Excel file
try:
    df = pd.read_excel(r"C:\Users\cdac\invitation\python\email_addresses1313.xlsx")
except Exception as e:
    print(f"Error loading Excel file: {e}")
    exit()

# Validate required columns
required_columns = ["To", "Name"]
for col in required_columns:
    if col not in df.columns:
        print(f"Missing required column: {col}")
        exit()

# Get file paths from command-line arguments
file_paths = sys.argv[1:]
for file_path in file_paths:
    if not os.path.exists(file_path):
        print(f"The file does not exist: {file_path}")
        exit()

# Function to compress files into a zip
def compress_files(file_paths):
    zip_file_name = "attachments.zip"
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            zipf.write(file_path, os.path.basename(file_path))
    return zip_file_name

# Compress files before sending
compressed_file = compress_files(file_paths)

# Function to validate email format using regex (updated for more valid formats)
def is_valid_email(email):
    # Regex updated to handle more cases (e.g., extra dot at the end, multiple-part TLDs)
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$'
    return re.match(email_regex, email) is not None

# Set up the SMTP server
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)  # Use App Password here

    # Iterate through rows and send emails
    for index, row in df.iterrows():
        recipient_email = row["To"]

        # Check if the email is valid
        if not is_valid_email(recipient_email):
            print(f"Invalid email address found: {recipient_email}. Skipping this email.")
            continue  # Skip sending the email for invalid addresses

        try:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = "Invitation for Capacity Building Programme"

            recipient_name = row["Name"]

            # HTML Email Body with Clickable Link and Attachment
            body = f"""\
            <html>
            <body>
                <p>Dear {recipient_name},</p>
                <p>You are invited to join the <b>CBP programming at CDAC Bangalore.</b></p>
                <p>We look forward to your participation in this exciting opportunity to enhance your skills.</p>
                <p><a href="https://www.cdac.in" target="_blank">Click here to register</a></p>
                <p>Please find the materials for the program in the attached files.</p>
                <p>Please feel free to reach out for any queries.</p>
                <p>Best regards,<br>CDAC Bangalore</p>
            </body>
            </html>
            """
            message.attach(MIMEText(body, "html"))  # Attach HTML content

            # Attach the compressed zip file
            with open(compressed_file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(compressed_file)}")
                message.attach(part)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())
            print(f"Email sent to {recipient_email}")

        except Exception as e:
            print(f"Error sending email to {recipient_email}: {e}")

    server.quit()
    print("All emails sent successfully!")

except Exception as e:
    print(f"Error: {e}")
