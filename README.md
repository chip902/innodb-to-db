# InnoDB File Parser and Email Extractor

This repository contains Python scripts to parse Innodb (IBD) files, filter relevant records containing email addresses, and extract those emails for further use. The scripts are designed to work together in a pipeline but can be run individually as well. Follow the instructions below for setup, usage, and understanding of each script's role in the system.

## Setup

1. Ensure you have Python 3 installed on your machine. This project was developed with Python 3.11.
2. Clone this repository to your local machine: `git clone https://github.com/chip902/inno-to-db.git`
3. Navigate to the root directory of the repository in your terminal/command line.
4. Install required packages using pip: `pip install -r requirements.txt`

## Script Descriptions

### app.py

The main script for parsing IBM files and filtering relevant records. The `process_ibd_directory` function reads IBD files, interprets their content based on a supplied schema, detects potential parent node pages (page types of 17854), and attempts to interpret each record as ASCII or return the raw binary data if decoding fails.

The `process_record` function processes a single record by searching for an email pattern within it. If there's a match, it returns `Record ID: id, Email: email`. Otherwise, it informs that no valid email was found for this record (`Record ID: id, No valid email found`).

### filter.py

This script is a post-processing utility that reads an input file line by line and writes those containing the substring 'billing_email' to an output file. This helps narrow down records with potential email addresses for further extraction without manually checking every record in `app.py`.

### extract_email.py

The final script in this pipeline, it reads a text file obtained from filter.py and extracts any valid email addresses that it can find using regular expressions. Extracted emails are then saved to 'extracted_emails.txt'.

## Usage

Run the commands below based on your needs:

-   To only parse files and print information, but not extract emails, run `python app.py`
-   After running `app.py`, use `python filter.py` to obtain a filtered list of records containing billing_email substring.
-   Run `python extract_email.py` on 'filtered_output.txt' to generate 'extracted_emails.txt', a list of all extracted emails from the provided IBD files.

## Contributions

Contributions to this project are welcome! To contribute please fork this repository and submit pull requests with your changes. Prior to submitting any significant modifications, ensure that they can be justified based on improved functionality or correcting bugs/issues you've found within the codebase. Please include relevant documentation within commit messages for easy reviewing.

## License

This project is licensed under the MIT License - see license file for details. All users are free to use this tool for personal and commercial purposes without asking for permission or attribution but should adhere to all applicable laws and regulations when doing so (including compliance with GDPR, CCPA, etc., where relevant). Contributors waive their moral rights to any contributions provided. By using these scripts, you agree that all responsibility falls on the user(s) of this project - including any damage caused by its use or misuse.
