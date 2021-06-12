# xml_processing.py
import xml.etree.ElementTree as ET

#Detect "GSM_INFO.xml" file in GameSave Manager zip file
def locate_gsm_info_in_zip(zip_ref):
    for fname, bio in zip_ref.readall().items():
        if fname == 'GSM_INFO.xml':
            return bio.read()
    return None
     
        
def validate_xml_string(gsm_file: str, xml_string: str, print_xml: bool = False):
    try:
        root = ET.fromstring(xml_string)
        if print_xml:
            print(xml_string.decode())
        return (root.tag == 'GameSaveManager_EntryData')
    except ET.ParseError as e:
        print(f"ERROR: Error parsing XML data in file: {gsm_file}. {str(e)}")