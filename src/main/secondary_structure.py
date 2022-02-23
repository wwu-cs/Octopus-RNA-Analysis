#!/usr/bin/python
'''
Identifying secondary structures given
    - FASTA file of genetic sequences
    - CSV file with potential edit sites
'''
import csv
import fastaparser
from Bio.Seq import Seq

def create_edit_dict(csv_file):
    '''
    Takes in:
        - csv file containing ids and edits.
    Returns:
        - edit_dict: ids as keys and list of edits as values.
    '''
    edit_dict = {}
    with open(csv_file, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['orf'] not in edit_dict:
                edit_dict[row['orf']] = [int(row['pos'])]
            else:
                edit_dict[row['orf']].append(int(row['pos']))
    return edit_dict

def secondary_structure(pos_list, sequence):
    '''
    Takes in:
        - pos_list: list of potential edit positions
        - sequence: genetic sequence corresponding to pos_list
    Returns:
        - len_list: list of secondary structure lengths for pos_list
    '''
    len_list = []
    for pos in pos_list:
        lo_ = pos
        hi_ = pos + 1
        for i in range(len(sequence)): # pylint: disable=unused-variable
            rev_comp = str(Seq(sequence[lo_:hi_]).reverse_complement())
            if rev_comp not in sequence:
                break
            if ((rev_comp in sequence) and (rev_comp not in sequence[lo_:hi_])):
                lo_ -= 1
                hi_ += 1
        len_list.append(len(rev_comp))
    return len_list

def find_secondary_structures(edit_dict, fasta_file):
    '''
    Takes in:
        - edit_dict: ids as keys and list of edits as values
        - fasta_file: file containing all genetic sequences
    Returns:
        - score_dict: ids as keys and scores (length for now) as values
    '''
    score_dict = {}
    with open(fasta_file, encoding="utf8") as fastafile:
        parser = fastaparser.Reader(fastafile)
        for seq in parser:
            if seq.id in edit_dict:
                score_dict[seq.id] = secondary_structure(edit_dict[seq.id],
                                                         seq.sequence_as_string())
    return score_dict

def create_output_csv(file_name, score_dict):
    '''
    Takes in:
        - file_name: name of output csv file to be created
        - score_dict: ids as keys and scores (length for now) as values
    Creates:
        - output csv file
    '''
    with open(file_name, 'w', newline='', encoding="utf8") as csvfile:
        fieldnames = ['id', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for id_, score in score_dict.items():
            writer.writerow({'id': id_, 'score': score})