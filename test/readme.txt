The three files ip.bam, input.bam and example.gtf can be used to run this software, and the run command is:

cd path_to_the_metaqc_directory/test
metaqc -p ip.bam -u input.bam -t SE -s hg19 -g example.gtf -o test
