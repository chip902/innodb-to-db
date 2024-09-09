import re


def extract_emails(file_path, output_path):
    with open(file_path, 'r') as infile, open(output_path, 'w') as outfile:
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

        for line in infile:
            matches = re.findall(email_pattern, line)
            if matches:
                for email in matches:
                    outfile.write(email + '\n')


# Specify the input file and output file
input_file = 'filtered_output.txt'
output_file = 'extracted_emails.txt'

# Run the extraction
extract_emails(input_file, output_file)

print(f"Email extraction complete. Check the output file: {output_file}")
