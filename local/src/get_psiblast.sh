#!/bin/bash

PROJECT='/home/vince/lsbPJ/project'
PROFILE=$PROJECT'/profile_gen'

for i in `cat $PROJECT/jpred4.list.txt`
do
psiblast -query $PROJECT/fasta/$i.fasta -db $PROFILE/uniprot_sprot.fasta -evalue 0.01 -num_iterations 3 -out_ascii_pssm $PROFILE/pssm/$i.pssm -num_descriptions 10000 -num_alignments 10000 -out $PROFILE/aln/$i.alns.blast
done