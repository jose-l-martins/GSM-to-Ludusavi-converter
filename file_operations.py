# file_operations.py
import hashlib
import py7zr
import zipfile


def compute_sha1(data):
    sha1 = hashlib.sha1()
    sha1.update(data)
    return sha1.hexdigest()


def extract_and_check_files_in_gsba(archive_path: str, inner_folder_path: str):
    results = {}
    
    # Check if the file ends in .gsba
    if not archive_path.endswith('.gsba'):
        raise ValueError(f"ERROR: File {archive_path} does not end in .gsba")
    
    # Check if its a .7z file
    if py7zr.is_7zfile(archive_path):
        with py7zr.SevenZipFile(archive_path, mode='r') as z:
            extracted_files = z.read()

            # Process the extracted data further or store it for later use
            for file_path, file_data_io in extracted_files.items():
                # Skip directories and process files within the inner folder
                if not file_path.endswith('/') and file_path.startswith(inner_folder_path):
                    # Convert BytesIO object to bytes-like object
                    file_data = file_data_io.getvalue()
                    # Compute SHA-1 hash and uncompressed size, in bytes
                    sha1_hash = compute_sha1(file_data)
                    uncompressed_size = len(file_data)
                    results[file_path] = {
                        'hash': sha1_hash,
                        'size': uncompressed_size
                    }
    # Check if its a .zip file                
    elif zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            extracted_files = zip_ref.namelist()

            # Process the extracted data further or store it for later use
            for file_path in extracted_files:
                # Skip directories and process files within the inner folder
                if not file_path.endswith('/') and file_path.startswith(inner_folder_path):
                    # Convert BytesIO object to bytes-like object
                    file_data = zip_ref.read(file_path)
                    # Compute SHA-1 hash and uncompressed size, in bytes
                    sha1_hash = compute_sha1(file_data)
                    uncompressed_size = len(file_data)
                    results[file_path] = {
                        'hash': sha1_hash,
                        'size': uncompressed_size
                    }
    else:
        raise ValueError(f"ERROR: File {archive_path} is not a .7z or .zip file, at heart. The .gsba file might be corrupted.")
    
    return results