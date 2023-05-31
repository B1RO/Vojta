import os
import traceback
from multiprocessing import Pool
import lxml.etree as ET
from tqdm import tqdm

# Function to process an individual XML file
def process_file(xml_file_name):
    xml_dir_path = './compounds/'
    xml_file_path = os.path.join(xml_dir_path, xml_file_name)

    # Use iterparse to parse the XML file incrementally
    context = ET.iterparse(xml_file_path, events=("start", "end"))

    total_elements = 500000
    pbar = tqdm(total=total_elements, desc=f"Processing elements in {xml_file_name}", unit="elements")

    out_file_path = os.path.join(xml_dir_path, os.path.splitext(xml_file_name)[0] + '.tsv')

    with open(out_file_path, "a") as myfile:
        myfile.write("CID\t SMILES\t IUPAC\n")
        for event, elem in context:
            try:
                if event == "start" and elem.tag == "{http://www.ncbi.nlm.nih.gov}PC-Compound":
                    pbar.update()
                    id_node = elem.find(".//{http://www.ncbi.nlm.nih.gov}PC-CompoundType_id_cid")
                    if id_node is None:
                        continue

                    id = id_node.text
                    smiles = None
                    iupac = None

                    props = elem.find(".//{http://www.ncbi.nlm.nih.gov}PC-Compound_props")
                    if props is not None:
                        smiles_children = [child for child in props.iter() if
                                           child.tag == '{http://www.ncbi.nlm.nih.gov}PC-Urn_label' and child.text == 'SMILES' and child.getparent().find(
                                               '{http://www.ncbi.nlm.nih.gov}PC-Urn_name') is not None and child.getparent().find(
                                               '{http://www.ncbi.nlm.nih.gov}PC-Urn_name').text == 'Isomeric']
                        if len(smiles_children) > 0:
                            smiles_node = smiles_children[0].getparent().getparent().getparent().find(
                                './/{http://www.ncbi.nlm.nih.gov}PC-InfoData_value_sval')
                            if smiles_node is not None:
                                smiles = smiles_node.text

                        iupac_children = [child for child in props.iter() if
                                          child.tag == '{http://www.ncbi.nlm.nih.gov}PC-Urn_label' and child.text == 'IUPAC Name' and child.getparent().find(
                                              '{http://www.ncbi.nlm.nih.gov}PC-Urn_name') is not None]
                        if len(iupac_children) > 0:
                            iupac_node = iupac_children[0].getparent().getparent().getparent().find(
                                './/{http://www.ncbi.nlm.nih.gov}PC-InfoData_value_sval')
                            if iupac_node is not None:
                                iupac = iupac_node.text

                    if id is not None and smiles is not None and iupac is not None:
                        myfile.write(id + "\t" + smiles + "\t" + iupac + "\n")

            except Exception as e:
                traceback.print_exc()
                print(f"Error occurred: {e}")
            finally:
                elem.clear()

    pbar.close()

def main():
    # Get the list of XML files
    xml_dir_path = './compounds/'
    xml_files = [f for f in os.listdir(xml_dir_path) if f.endswith('.xml')]

    # Create a pool of worker processes
    pool = Pool()

    # Use the pool to process the files in parallel
    pool.map(process_file, xml_files)

    # Close the pool and wait for the worker processes to finish
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()
