import os
import argparse
import glob
import py7zr
from gsm_xml_processor import locate_gsm_info_in_zip, validate_xml_string
from ludusavi_mapping_generator import create_ludusavi_mapping


# Function to process GameSave Manager backup files in a folder
def process_gsm_folder(folder_path: str,output_yaml_file_path: str):
    gsm_files = glob.glob(os.path.join(folder_path, '*.gsba'))
    ludusavi_mappings = []

    for gsm_file in gsm_files:
        seven_z_file = gsm_file
        print(f"Processing .gsba file: {seven_z_file}")

        with py7zr.SevenZipFile(seven_z_file, 'r') as zip_ref:
            xml_string = locate_gsm_info_in_zip(zip_ref)

            if not xml_string:
                print(f"ERROR: No GSM_INFO.xml file found in: {gsm_file}")
            else:
                parsing_processing_flag = validate_xml_string(gsm_file, xml_string, print_xml=False)
                  
            if parsing_processing_flag:
                ludusavi_mapping = create_ludusavi_mapping(gsm_file, xml_string, output_yaml_file_path)
                ludusavi_mappings.append(ludusavi_mapping)
                
    return ludusavi_mappings


def main():     
    parser = argparse.ArgumentParser(description='Process GameSave Manager backup files and generate Ludusavi mappings.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing GSM backup files')
    parser.add_argument('output_yaml_file_path', type=str, help='Path to the output folder for Ludusavi YAML files')
    args = parser.parse_args()


    try:
        process_gsm_folder(args.folder_path, args.output_yaml_file_path)
    except Exception as e:
        print(f"ERROR: {e}")
        raise e


if __name__ == "__main__":
    main()