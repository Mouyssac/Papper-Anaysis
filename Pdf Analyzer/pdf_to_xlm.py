import subprocess

def convert_pdf_to_xml(pdf_path, xml_path):
    # Commande pour utiliser pdf2xml
    command = f'pdf2xml "{pdf_path}" -o "{xml_path}"'
    subprocess.run(command, shell=True)

pdf_file = 'C:/Users/maxim/Desktop/Projets_perso/papper mapping tests/Article.pdf'
xml_file = 'C:/Users/maxim/Desktop/Projets_perso/papper mapping tests/Article.xml'

convert_pdf_to_xml(pdf_file, xml_file)