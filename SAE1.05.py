import re
import csv
import os
import markdown
import webbrowser
from tkinter import filedialog
from tkinter import Tk


Tk().withdraw()
dump_file_path = filedialog.askopenfilename()

csv_file_path1 = "source.csv"
csv_file_path2 = "destination.csv"

def parse_dump_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    source_packet_counts = {}
    destination_packet_counts = {}
    for line in lines:
        if re.match(
            r"(\d+:\d+:\d+\.\d+) IP (.+?) > (.+?):",
            line,
        ):
            match = re.match(
                r"(\d+:\d+:\d+\.\d+) IP (.+?) > (.+?):",
                line,
            )
            
            source = match.group(2)
            destination = match.group(3)
            
            if 'solunet.com.ar' in source:
                source = 'gba.solunet.com.ar'
            if 'solunet.com.ar' in destination:
                destination = 'gba.solunet.com.ar'
                    
            if 'par' in source:
                source = 'Paris'
            if 'par' in destination:
                destination = 'Paris'
                
            if 'BP' in source:
                source = 'Linux'
            if 'BP' in destination:
                destination = 'Linux'
            # Compter les paquets source
            if source:
                if source in source_packet_counts:
                    source_packet_counts[source] += 1
                else:
                    source_packet_counts[source] = 1
            # Compter les paquets destination
            if destination:
                if destination in destination_packet_counts:
                    destination_packet_counts[destination] += 1
                else:
                    destination_packet_counts[destination] = 1
    # Trier les dictionnaires source_packet_counts et destination_packet_counts par ordre décroissant du compteur
    source_packet_counts = dict(sorted(source_packet_counts.items(), key=lambda x: x[1], reverse=True))
    destination_packet_counts = dict(sorted(destination_packet_counts.items(), key=lambda x: x[1], reverse=True))
    
    return source_packet_counts, destination_packet_counts

def save_to_csv(packet_counts, csv_file_path):
    with open(csv_file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")
        # Écrire l'en-tête CSV
        csv_writer.writerow(
            [
                "Adresse",
                "Nombre de paquets"
            ])
        for address, count in packet_counts.items():
            # Écrire les informations dans le fichier CSV
            csv_writer.writerow(
                [
                    address,
                    count,
                ])
            
# Charger les données à partir du fichier CSV
source_packet_counts, destination_packet_counts = parse_dump_file(dump_file_path)
# Sauvegarder les paquets source dans le fichier source.csv
save_to_csv(source_packet_counts, csv_file_path1)
print("Les données ont été enregistrées dans", csv_file_path1)       

# Sauvegarder les paquets destination dans le fichier destination.csv
save_to_csv(destination_packet_counts, csv_file_path2)
print("Les données ont été enregistrées dans", csv_file_path2)  


markdown_content = ('''
<style>
table{
    border: 1px black solid;
    border-collapse: collapse;
}
#tableau1{
    border: 2px black solid;
    border-collapse: collapse;
}
th{
    border: 1px black solid;
}
td{
    border: 1px black solid;
}
#tableau2{
    border: 2px black solid;
    border-collapse: collapse;
    margin-top: 30px
}
</style>
<table id='tableau1')>
<caption>Tableau des Sources</caption>
<tr>
<th>Source</th>
<th>Nombre</th>
<th>Suspect ?</th>
</tr>
''')

# Charger les données du fichier source.csv
with open(csv_file_path1, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    next(csv_reader)  # Ignorer l'en-tête CSV

    for row in csv_reader:
        source = row[0]
        nombre = row[1]
        if int(nombre) > 1500:
            suspect = "Oui"
        else:
            suspect = "Non"
        markdown_content += f"<tr><td>{source}</td><td>{nombre}</td><td>{suspect}</td></tr>"

markdown_content += ('''</table>
<table id='tableau2'>
<caption>Tableau des Destination</caption>
<th>Destination</th>
<th>Nombre</th>
<th>Suspect ?</th>
''')

# Charger les données du fichier destination.csv
with open(csv_file_path2, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=";")
    next(csv_reader)  # Ignorer l'en-tête CSV

    for row in csv_reader:
        destination = row[0]
        nombre = row[1]
        if int(nombre) > 1500:
            suspect = "Oui"
        else:
            suspect = "Non"
        markdown_content += f"<tr><td>{destination}</td><td>{nombre}</td><td>{suspect}</td></tr>"
markdown_content += "</table>"

# Enregistrer le contenu markdown dans un fichier puis le confvertir en html
markdown_file_path = "tables.md"
with open(markdown_file_path, "w") as markdown_file:
    markdown_file.write(markdown_content)
html_file_path = "tables.html"
with open(markdown_file_path, "r") as markdown_file:
    markdown_text = markdown_file.read()
    html_text = markdown.markdown(markdown_text)

with open(html_file_path, "w") as html_file:
    html_file.write(html_text)


#ouvrir les données
#os.startfile(csv_file_path1)     
#os.startfile(csv_file_path2)

webbrowser.open(html_file_path)
