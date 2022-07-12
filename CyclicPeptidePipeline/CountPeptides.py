from Bio import SeqIO
import pickle
import sys
import os


SOURCE_FOLDER = sys.argv[1] # Nom du fichier qu'on veut split, qui doit être dans le même répertoire. Importé comme un argument du programme.
DESTINATION_FOLDER = sys.argv[2]
FILE_TYPE = "fasta"

# Vérification de la longueur des peptides
PEPTIDE_LENGTH = 12
NUCLEOTIDES = list("ACGT")

def check_size(FILE, size=PEPTIDE_LENGTH):
    """ Parcours l'intégralité du fichier FILE pour déterminer si les peptides ont la même longueur"""
    for record in SeqIO.parse(FILE, FILE_TYPE):
        if len(record) != size:
            return
    return True

# Comptage


def get_count_dna(fasta_file, peptides=dict()):
    """Compte l'occurence de chaque peptide.
    Sortie: un dictionnaire dont les clés sont des séquences (objet seq)"""
    count = 0
    indiv_count = 0
    for record in SeqIO.parse(fasta_file, FILE_TYPE):
        count = count + 1
        if count % 1000000 == 0:
            print("We have processed " + str(count) + " records.") #Just so I know it is running
        try:
            peptides[record.seq] += 1
        except:
            peptides[record.seq] = 1
            indiv_count = indiv_count + 1
    print("We have processed " + str(count) + " records, containing " + str(indiv_count) + " unique sequences.")
    return peptides

def get_count_aa(fasta_file, peptides=dict()):
    """Compte l'occurence de chaque peptide.
    Sortie: un dictionnaire dont les clés sont des séquences (objet seq)"""
    count = 0
    indiv_count = 0
    for record in SeqIO.parse(fasta_file, FILE_TYPE):
        count = count + 1
        if count % 1000000 == 0:
            print("We have processed " + str(count) + " records.") #Just so I know it is running
        try:
            peptides[record.translate().seq] += 1
        except:
            peptides[record.translate().seq] = 1
            indiv_count = indiv_count + 1
    print("We have processed " + str(count) + " records, containing " + str(indiv_count) + " unique sequences.")
    return peptides


# Pour sauvegarder le fichier
# NB : avec pickle on sauvegarde un seul objet
# This leads to a highly efficient binary file but one that can't easily be processed. 

# Get the list of .fa files to process
file_list = []

for file in os.listdir(SOURCE_FOLDER):
    if file.endswith(".fa"):
        file_list.append(file)

# Treat the files and save the pickled results

for file in file_list:
    output_file_name = file.replace(".fa", "_count_aa_pickle")
    saved_file = open(DESTINATION_FOLDER+"\\"+output_file_name, mode="ab")
    peptides = get_count_aa(SOURCE_FOLDER+"\\"+file)
    pickle.dump(peptides, saved_file)

# Readable_file = open("Count Saves bis", mode="rb")
# peptides = pickle.load(Readable_file)
# # print(peptides) permet l'affichage du dictionnaire
