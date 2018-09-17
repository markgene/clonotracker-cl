mkdir -p data
cd data
# FASTQ file1
curl -O ftp://ftp.ddbj.nig.ac.jp/ddbj_database/dra/fastq/SRA148/SRA148517/SRX497280/SRR1200517_1.fastq.bz2
bzip2 -d SRR1200517_1.fastq.bz2
seqtk sample -s100 SRR1200517_1.fastq 10000 > sub1.fq
rm -f SRR1200517_1.fastq
# FASTQ file2
curl -O ftp://ftp.ddbj.nig.ac.jp/ddbj_database/dra/fastq/SRA148/SRA148517/SRX497280/SRR1200517_2.fastq.bz2
bzip2 -d SRR1200517_2.fastq.bz2
seqtk sample -s100 SRR1200517_2.fastq 10000 > sub2.fq
rm -f SRR1200517_2.fastq
cd ..
