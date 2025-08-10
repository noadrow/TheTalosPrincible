#import Bio.SeqIO as SeqIO
import re
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog


# This script search for patterns in fasta file format
# It creates bed and fasta files for each sequence that has that pattren
# Please Note:
# This script takes only the file name "fileToSearch"
# This script search and create files that located at the same folder of the script
# This script uses regx for special nuclotide notation (such as N) you can place all nucletodies under []
def SeqIO_parse(fileToSearch):
    with open(fileToSearch, "r") as file:
        seq_data = {"id":[],"seq":[]}
        flag = False
        seq = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                flag = not flag
                seq_id = line[1:]
                seq_data["id"].append(seq_id) # Remove '>' and take the ID
            else:
                seq = seq + line

            if not flag:
                seq_data["seq"].append(seq)
                seq = ""
                flag = not flag

    return seq_data


dfs = []
files = []
searchlist = []
pattrenList = []
#fileToSearch = "GFR_positive"
fileToSearch = askopenfilename(title="Select fasta")
#pattrensToSearch = ['TGA[AG]TCA','ATTCC','CCGGAA']
pattrensToSearch = simpledialog.askstring("enter motif sequence", "Enter a string:")

def searchSeq(x):
        dfs.append(["",""])
        files.append([open(fileToSearch+"_"+x+".fa","w"),open(fileToSearch+"_"+x+".bed","w")])
        pattrenList.append(re.compile(x))
   
searchSeq(pattrensToSearch)

#save input files and data frames
temp_df = []
temp_df += files

open("protocol_dfs_log.txt","w").write(str(files))

for (file, df, pattern) in zip(files,dfs,pattrenList):
    seq_record = SeqIO_parse(fileToSearch)
    for i in range(len(seq_record["seq"])):
        seqId = seq_record["id"][i]
        seq = str(seq_record["seq"][i]).upper()

        if pattern.findall(seq):
            df[0] += f">{seqId}\n{seq}\n"

            ##UCSC seqID format
            #chr = seqId.split("=")[1].split(":")[0]
            #start = seqId.split("=")[1].split(":")[1].split("-")[0]
            #end = seqId.split("=")[1].split(":")[1].split("-")[1].split(" ")[0]

            ## bedtools getfasta seqID format
            chr = seqId.split(":")[0]
            start = seqId.split(":")[1].split("-")[0]
            end = seqId.split(":")[1].split("-")[1]
            df[1] += f"{chr}\t{start}\t{end}\n"

    file[0].write(df[0])
    file[0].close()

    file[1].write(df[1])
    file[1].close()
