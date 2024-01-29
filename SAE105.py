import os
import csv
import pandas as pd
import subprocess
import re
import markdown
import webbrowser
from collections import Counter

#C:\R.T\SAE1.05\portfolio sae1.05\Données traites\DumpFile.txt 
#C:\R.T\SAE1.05\portfolio sae1.05\donnéestraités.csv 

#dump_file_path = input("Entrer votre chemin pour le fichier a analyser : \n")
#csv_file_path = input("Entrer votre chemin pour le fichier avec le '.csv' : \n")

dump_file_path = 'DumpFile.txt'
csv_file_path = 'donnéestraités.csv'

packet_data = []
with open(dump_file_path, 'r') as f:
    for line in f:
        match = re.match(
            r"(\d+:\d+:\d+\.\d+) IP (.+?) > (.+?):.* length (\d+)",
            line,
        )
        if match:
            source = match.group(2)
            destination = match.group(3)
                
            if 'https' in source or re.search(r'\d{5}', source):
                source = re.sub(r'.\d{5}', '', source)
            if 'https' in destination or re.search(r'\d{5}', destination):
                destination = re.sub(r'.\d{5}', '', destination)

            if 'https' in source:
                source = 'https'
            if 'https' in destination:
                destination = 'https'

            if 'solunet.com.ar' in source:
                source = '190-0-175-100.gba.solunet.com.ar'
            if 'solunet.com.ar' in destination:
                destination = '190-0-175-100.gba.solunet.com.ar'

            if 'BP-Linux' in source:
                source = 'BP-Linux'
            if 'BP-Linux' in destination:
                destination = 'BP-Linux'

    
            packet_data.append({
                "timestamp": match.group(1),
                "Source": source,
                "destination": destination,
                "Lenght":match.group(4)
            })

df = pd.DataFrame(packet_data)
df.to_csv(csv_file_path, index=False, sep=';', encoding='utf-8-sig')

print(f"Les données ont été enregistrées dans {csv_file_path}.")
webbrowser.open(csv_file_path)



