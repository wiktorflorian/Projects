import csv
import os
import math

def split_csv(input_path, output_dir, max_file_size_mb, delimiter=';', output_file_name = 'chunk'):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Calculate the maximum chunk size in decimal bytes
    max_file_size = max_file_size_mb * 1000 * 1000
    
    # Get the size of the input file
    file_size = os.path.getsize(input_path)
    
    # Calculate the approximate total number of chunks
    total_n_chunks = math.ceil(file_size / max_file_size)
    
    # Initialize variables
    current_chunk = 1
    output_file = os.path.join(output_dir, f"{output_file_name}_{current_chunk}.csv")

    # Read the input file and extract rows
    with open(input_path, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

        # Get the heade row
        header_row = rows[0]
        header_row_str = delimiter.join(header_row) + '\n'
        current_file_size = len(header_row_str)
    
    # Iterate over rows and split into chunks
    for row in rows:
        row_str = delimiter.join(row) + '\n'
        row_size = len(row_str)

        if current_file_size + row_size > max_file_size:
            print(f"Saved {current_chunk} / {total_n_chunks}")

            # Increment chunk number
            current_chunk += 1
            output_file = os.path.join(output_dir, f"{output_file_name}_{current_chunk}.csv")

            with open(output_file, 'w', newline='') as f_new:
                writer = csv.writer(f_new, delimiter=delimiter)
                writer.writerow(header_row)

            current_file_size = len(header_row_str)
        
        with open(output_file, 'a', newline='') as f_out:
            writer = csv.writer(f_out, delimiter=delimiter)
            writer.writerow(row)

            current_file_size += row_size
    
    print(f"Saved {current_chunk} / {total_n_chunks}")