import struct
import os
import re

# Updated schema for wp_newsletter table
wp_newsletter_schema = {
    'id': 'int',
    'email': 'string',
    'list_1': 'bool',
    'list_2': 'bool',
    'profile_1': 'string',
    'profile_2': 'string'
}

# Set the directory path containing the .ibd files
ibd_directory = "/Users/andrew/Downloads/mysql/skydb"

# Function to parse individual records based on schema


def parse_record(record_bytes, schema):
    """
    Parse a record from raw bytes using the given schema.
    """
    offset = 0
    record_data = {}

    for field_name, field_type in schema.items():
        if field_type == 'int':
            length = 4  # Assuming 4 bytes for integers
            value = int.from_bytes(
                record_bytes[offset:offset + length], byteorder="big")
            offset += length
        elif field_type == 'string':
            length = 255  # Assuming max 255 characters for strings
            value = record_bytes[offset:offset +
                                 length].decode('utf-8', errors='ignore').strip('\x00')
            offset += length
        elif field_type == 'bool':
            length = 1  # Assuming 1 byte for boolean fields
            value = bool(record_bytes[offset])
            offset += length

        record_data[field_name] = value

    return record_data


# Function to parse a page and extract records
def parse_page(page, schema):
    """
    Parse the records from a given page.
    """
    page_type = int.from_bytes(page[24:26], byteorder="big")

    if page_type == 17855:  # Leaf node containing records
        print("Parsing records from page...")
        # Typically, records would start after the header and directory in the page
        header_size = 38
        directory_size = 2 * 16  # Assuming 16 slots in the page directory
        record_start = header_size + directory_size

        while record_start < len(page):
            # Estimate record size
            record_bytes = page[record_start:record_start + 400]
            if len(record_bytes) == 0:
                break

            # Parse the record using the schema
            record = parse_record(record_bytes, schema)

            # Output the parsed record
            print(f"Record: {record}")

            # Move to the next record (this estimate may need adjustment)
            record_start += 400


def process_ibd_file(file_path, schema):
    """
    Process an individual .ibd file.
    """
    print(f"Processing file: {file_path}")

    with open(file_path, "rb") as f:
        page_size = 16 * 1024  # InnoDB pages are 16KB
        page_number = 0

        while True:
            page = f.read(page_size)
            if not page:
                break

            page_number, page_type = parse_page_header(page)
            print(f"Page Number: {page_number}, Page Type: {page_type}")

            # Parse the page if it's of the correct type
            if page_type == 17855:
                parse_page(page, schema)

            page_number += 1


def process_ibd_directory(ibd_directory, schema):
    """
    Process all .ibd files in a directory.
    """
    for root, dirs, files in os.walk(ibd_directory):
        for file in files:
            if file.endswith(".ibd"):
                file_path = os.path.join(root, file)
                process_ibd_file(file_path, schema)


def parse_page_header(page):
    """
    Parse the header of a page to extract the page number and page type.
    """
    header = page[:38]  # Page header is the first 38 bytes
    page_number = int.from_bytes(header[4:8], byteorder="big")
    page_type = int.from_bytes(header[24:26], byteorder="big")
    return page_number, page_type


def traverse_parent_nodes(ibd_directory):
    parent_nodes = {}  # Dictionary to store parent nodes for each file

    # Debugging: Print the directory being processed
    print(f"Processing directory: {ibd_directory}")

    for root, dirs, files in os.walk(ibd_directory):
        for file in files:
            if file.startswith("wp_newsletter"):
                file_path = os.path.join(root, file)

                # Debugging: Print the file being processed
                print(f"Processing file: {file_path}")

                with open(file_path, "rb") as f:
                    page_size = 16 * 1024  # InnoDB pages are 16KB
                    page_count = 0

                    while True:
                        page = f.read(page_size)
                        if not page:
                            break

                        page_number, page_type = parse_page_header(page)

                        # Debugging: Print the page number and type for every page
                        print(f"File: {file_path}, Page Number: {
                              page_number}, Page Type: {page_type}")

                        # Check if the page is an internal node (parent)
                        if page_type == 17854:
                            print(f"Found parent node in {
                                  file}: Page Number {page_number}")
                            if file not in parent_nodes:
                                parent_nodes[file] = []
                            parent_nodes[file].append(page_number)
                        page_count += 1

                    # Debugging: Print how many pages were processed from this file
                    print(f"Processed {page_count} pages from {file_path}")

    return parent_nodes


def decode_binary_data(record_bytes):
    try:
        # Try to decode as ASCII
        # 'ignore' will skip invalid characters
        return record_bytes.decode('ascii', errors='ignore')
    except Exception as e:
        # If decoding fails, return raw binary data as a string
        return str(record_bytes)


def process_record(record):
    """
    Processes a record to extract any email-like strings.
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Join all fields into a single string to search for an email
    record_string = ' '.join([str(value) for value in record.values()])

    # Look for a valid email pattern in the decoded data
    match = re.search(email_pattern, record_string)

    if match:
        return f"Record ID: {record['id']}, Email: {match.group(0)}"
    else:
        return f"Record ID: {record['id']}, No valid email found"


# Main script entry point
if __name__ == "__main__":
    # Call your function to process the directory or individual files
    parent_nodes = traverse_parent_nodes(ibd_directory)
    print("Parent Nodes:", parent_nodes)

    process_ibd_directory(ibd_directory, wp_newsletter_schema)
