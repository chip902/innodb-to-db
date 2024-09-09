
# Open the input and output files
with open('out.txt', 'r') as infile, open('filtered_output.txt', 'w') as outfile:
    for line in infile:
        if 'billing_email' in line:
            # Write the line to the output file if it contains an '@' symbol
            outfile.write(line)

print("Filtering complete! Saved filtered rows to 'filtered_output.txt'")
