# file_operations.py
import hashlib
import py7zr


def compute_sha1(data):
    sha1 = hashlib.sha1()
    sha1.update(data)
    return sha1.hexdigest()


def extract_and_check_files_in_7z(archive_path, inner_folder_path):
    results = {}

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

    return results