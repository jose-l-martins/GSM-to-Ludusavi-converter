# ludusavi_mapping.py
import os
import re
import yaml
import xml.etree.ElementTree as ET
from date_formatting import convert_filename_to_hybrid_timestamp, convert_filename_to_iso_timestamp
from special_path_resolver import resolve_special_path
from file_operations import extract_and_check_files_in_gsba



def create_ludusavi_mapping(gsm_file: str, xml_string: str, output_yaml_file_path: str):
    ludusavi_mapping = {}
    
    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Accessing GameName element and saving it in YAML
    game_name_element = root.find('GameName')
    if game_name_element is not None:
        game_name = game_name_element.text
        ludusavi_mapping['name'] = "\"" + str(game_name) + "\""
                
    ludusavi_mapping["drives"] = {}
    ludusavi_mapping["backups"] = {}
    ludusavi_mapping["backups"]["- name"] = "backup-{}.zip".format(convert_filename_to_iso_timestamp(gsm_file))
    ludusavi_mapping["backups"]["when"] = "\"" + convert_filename_to_hybrid_timestamp(gsm_file, True) + "\""
    ludusavi_mapping["backups"]["os"] = "windows"
    ludusavi_mapping["backups"]["files"] = {}

    # Accessing Directory elements
    directories = root.findall('Directory')
    for directory in directories:
        special_path_element = directory.find('SpecialPath')
        if special_path_element is not None:
            special_path = special_path_element.text
            special_path_expanded = resolve_special_path(special_path) #os.path.expandvars(special_path)
            drive_letter = special_path_expanded[0]
            #e.g. {"drives": {"drive-C": "C:"}}
            ludusavi_mapping['drives']['drive-{}'.format(drive_letter)] = "\"" + drive_letter + ":" + "\""

        path_element = directory.find('Path')
        if path_element is not None:
            path = path_element.text
            full_folder_path = special_path_expanded + "\\" + path 
            
        files = directory.find("FileList").findall("File")
        all_file_names = [file.text for file in files]

        if gsm_file.endswith(".gsba"):
            inner_folder_index = directories.index(directory) + 1
            results_dict = extract_and_check_files_in_gsba(gsm_file, str(inner_folder_index)+ "/")

            for current_file_name in all_file_names:
                current_file_path = full_folder_path + "\\" + current_file_name
                key = "\"" + current_file_path + "\""
                hash_value = results_dict[(str(inner_folder_index)+ "\\" + current_file_name).replace("\\", "/")]["hash"]
                size_value = results_dict[(str(inner_folder_index)+ "\\" + current_file_name).replace("\\", "/")]["size"]
                ludusavi_mapping["backups"]["files"][key] = {"hash": hash_value, "size": size_value}
            
    ludusavi_mapping["backups"]["registry"] = {"hash": "~"}
    ludusavi_mapping["backups"]["children"] = []
    data = ludusavi_mapping

    # Dump the dictionary to a YAML file
    file_path = os.path.join(output_yaml_file_path, "mapping.yaml")
    try:
        with open(file_path, "w") as file:
            # Dump the dictionary to a YAML file without quotes around string values
            yaml.dump(data, file, sort_keys=False, explicit_start=True, default_style='',  default_flow_style=False, allow_unicode=True, encoding='utf-8') #indent=4 (maybe)
    except FileExistsError:
        print("File already exists. Avoided overwriting.")
        
    # Read the content of the YAML file
    with open(file_path, 'r') as file:
        content = file.read()

    # Remove all ' characters from the content, except those that are in the middle of a word, to keep titles like e.g. "Assassin's Creed"
    modified_content = re.sub(r"(?<!\w)'(?!'\w)", "", content)
    modified_content = re.sub(r"'(?=[:])", '', modified_content)

    #Replace all the backslasses (\) with forward slashes (/), in paths
    modified_content = modified_content.replace('\\', '/')
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Modify lines by adding a tab space to lines below '- name', not including '- name' line
    tabbed_content = []
    add_two_spaces = False  # Flag to indicate whether to add twos spaces "  " (Attention: it's not a tab space "\t")

    for line in content:
        if add_two_spaces:
            line = f'  {line}'
        if line.strip().startswith('- name'):
            add_two_spaces = True
        tabbed_content.append(line)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(tabbed_content)    