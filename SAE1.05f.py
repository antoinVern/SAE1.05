import markdown
import webbrowser
import re
import csv
import os
from tkinter import Tk, filedialog

# Chemin du fichier CSV
csv_file_path = "donnéestraités.csv"

# Fonction pour demander à l'utilisateur de sélectionner un fichier texte
def select_dump_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
    return file_path

# Fonction pour analyser le contenu d'un fichier de vidage et extraire les informations pertinentes
def parse_dump_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    packet_counts = {}
    current_packet = None

    # Parcourir chaque ligne dans le fichier de vidage
    for line in lines:
        if re.match(
            r"(\d+:\d+:\d+\.\d+) IP (.+?) > (.+?):",
            line,
        ):
            # Nouveau paquet détecté
            if current_packet:
                packet_key = f'{current_packet["source"]}-{current_packet["destination"]}'
    
                if packet_key in packet_counts:
                    packet_counts[packet_key]["count"] += 1
                else:
                    current_packet["count"] = 1
                    packet_counts[packet_key] = current_packet

            # Extraire l'horodatage, la source et la destination de la ligne
            match = re.match(
                r"(\d+:\d+:\d+\.\d+) IP (.+?) > (.+?):",
                line,
            )
            
            source = match.group(2)
            destination = match.group(3)
            timestamp = match.group(1)
            
            # Modifier la source et la destination si certaines conditions sont remplies
            if 'solunet.com.ar' in source:
                source = 'solunet.com.ar'
            if 'solunet.com.ar' in destination:
                destination = 'solunet.com.ar'
                    
            if 'BP' in source:
                source = 'BP-Linux'
            if 'BP' in destination:
                destination = 'BP-Linux'
            
            # Créer un dictionnaire pour le paquet actuel
            current_packet = {
                "timestamp": match.group(1),
                "source": source,
                "destination": destination,     
            }

    # Traiter le dernier paquet s'il y en a
    if current_packet:
        packet_key = f'{current_packet["source"]}-{current_packet["destination"]}'
        
        if packet_key in packet_counts:
            packet_counts[packet_key]["count"] += 1
        else:
            current_packet["count"] = 1
            packet_counts[packet_key] = current_packet
    return list(packet_counts.values())

# Fonction pour enregistrer les données analysées dans un fichier CSV
def save_to_csv(packets, csv_file_path):
    with open(csv_file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=";")

        # Écrire l'en-tête CSV
        csv_writer.writerow(
            [
                "Timestamp",
                "Source",
                "Destination",
                "Nombre de paquets"
            ]
        )

        # Écrire les données dans le fichier CSV
        for packet in packets:
            csv_writer.writerow(
                [
                    packet["timestamp"],
                    packet["source"],
                    packet["destination"],
                    packet["count"],
                ]
            )

# Exemple d'utilisation : sélectionner un fichier de vidage, l'analyser, enregistrer les résultats dans un CSV et ouvrir le fichier CSV
dump_file_path = select_dump_file()
if dump_file_path:
    packets = parse_dump_file(dump_file_path)
    packets = sorted(packets, key=lambda packet: packet["count"], reverse=True)
    save_to_csv(packets, csv_file_path)
    print("Les données ont été enregistrées dans", csv_file_path)       
    os.startfile(csv_file_path)
else:
    print("Aucun fichier sélectionné.")

# Fonction pour analyser le fichier CSV et créer des représentations HTML et Markdown
def parse_dump_file(file_path):
    packets = []
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
}
</style>
<table id='tableau1')>
<caption>Tableau des Sources</caption>
<tr>
<th>Timestamp</th>
<th>Source</th>
<th>Destination</th>
<th>Nombre</th>
</tr>
''')
    with open(file_path, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next(csv_reader)  # Ignorer la ligne d'en-tête
        for row in csv_reader:
            # Extraire les données de la ligne CSV
            timestamp = row[0]
            source = row[1]
            destination = row[2]
            count = int(row[3])
            packets.append({
                "timestamp": timestamp,
                "source": source,
                "destination": destination,
                "count": count
            })
            # Ajouter une ligne au tableau au format Markdown
            markdown_content += f" <tr><td>{timestamp}</td><td>{source}</td><td>{destination}</td><td>{count}</td></tr>\n"
            with open('Fichier.md', 'w') as file:
                file.write(markdown_content)
            # Convertir le fichier Markdown en HTML
            html_content = markdown.markdown(markdown_content)
            # Créer le fichier HTML 
            with open('Fichier.html', 'w') as file:
                file.write(html_content)
                
        return packets

# Exemple d'utilisation : analyser le fichier CSV et ouvrir le fichier HTML généré
packets = parse_dump_file(csv_file_path)
webbrowser.open('Fichier.html')
