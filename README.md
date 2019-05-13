# MetaQC: the MeRIP-seq data analysis and quality control toolkit


<p align="justify">MetaQC is a python package used for MeRIP-seq data analysis and quality control. This package can report the following quality metrics:</p>

- Uniquely Mapping Ratio

<p align="justify">Uniquely mapping reads are the reads with mapping quality >= 30. MetaQC can filter the BAM files and get uniquely mapping reads. The Uniquely Mapping Ratio is the ratio of uniquely mapping read counts to  the total read counts.</p>

- Nonredundant Fraction (NRF)

<p align="justify">A useful library complexity metric is the fraction of nonredundant mapped reads in a data set (nonredundant fraction or NRF), which is the ratio between the number of positions in the genome that uniquely mappable reads map to and the total number of uniquely mappable reads.</p>

- PCR Bottleneck Coefficient (PBC)

<p align="justify">Another useful library complexity metric is the PCR bottleneck coefficient (PBC). PBC is the fraction of genomic locations with exactly one unique read versus those covered by at least one unique read. In particular, PBC=M1/M_DISTINCT where M1 is number of genomic locations where exactly one read maps uniquely while M_DISTINCT is  number of distinct genomic locations to which some read maps uniquely.</p>

- Contamination Ratio

<p align="justify">Contamination Ratio is the tRNA and rRNA contamination ratio. The tRNA and rRNA genomic coordinates were downloaded from UCSC website. If the positons in the genome that reads map to are located in tRNA or rRNA genomic coordinates, the corresponding reads are called tRNA or rRNA reads. Contamination Ratio is the ratio of the sum of rRNA and tRNA read counts to the total number of mapped reads.</p>

- Library Saturation

<p align="justify">Library saturation is presented by the saturation curve. The X axis represents the fraction between the number of randomly extracted reads and the number of total reads in a sample.  The number of genes detected is on the y-axis and each sample that was sequenced in the experiment has a curve on the plot. A valid gene is the gene which have at least 5 reads mapping to it.</p>

- Peak Calling

<p align="justify">Peak calling is a computational method used to identify areas in a genome that have been enriched with aligned reads. This python package identifies m6A peaks across the transcriptome in order to determine the enrichment and clustering of m6A peaks within individual transcripts. The peak calling procedure was performed as described by Meyer et al. with some modifications. Briefly, RefSeq exones from all known annotated transcript forms of each gene were split into windows approximately 25 nt in size. Bedtools was then used to determine the number of reads within each replicate that mapped to each window. The number of reads in the MeRIP sample was then compared to the number in the non-IP sample within each window and Fisher’s exact test was used to compute p-values for the windows of each replicate. Only those windows with p-values less than or equal to 0.05 in all samples were kept. Next, windows were merged, and then the number of reads within each sample that mapped to each merged windows was determined. Fisher’s exact test was again used to compute p-values for the merged windows of each replicate. These p-values were then adjusted using Benjamini-Hochberg. If the length of the merged windows is between 100 and 1000 nt, and the fdr value is less than or equal to 0.05, the merged windows are treated as the detected m6A peaks.</p>

- Reads Distribution Dispersion (RDD)

<p align="justify">Read distribution dispersion is the Standard Deviation of the number of reads mapped to transcripts. In particual, for individual transcript, exones were split into windows approximately 25 nt in size. Bedtools was used to determine the number of reads mapped to each window on individual transcript. The Standard Deviation value of individual transcript was obtained. One transcript, one Standard Deviation value. These Standard Deviation values were represented by box plot. The median of Standard Deviation was used as RDD. In theory, the RDD value of IP sample is bigger than INPUT sample.</p>

- Fraction of Reads in Peaks (FRiP)

<p align="justify">FRiP is the fraction of all mapped reads that fall into peak regions identified by a peak-calling algorithm. To be specific, It is the ratio of the number of mapped reads in peaks to the number of all mapped reads. Typically, a minority of reads occur in significantly enriched genomic regions (i.e., peaks) while the remainder of the reads represents background. FRiP is therefore a useful and simple first-cut metric for the success of the immunoprecipitation.</p>

- Metagene

<p align="justify">Mapping m6A modifications sites throughout the transcriptome is very important to know where in the transcript do m6A sites preferentially occur, which can further provides clues to their functions. A metagene is a frequency plot of m6A sites along a transcript model containing a 5’UTR, CDS and 3’UTR. It is a simple and effective tool for visualizing the distribution of m6A sites.
</p>

- Peak Length Distribution

<p align="justify">Peak length distribution is presented by the histogram. The X axis represents the length of peaks. The number of peak is on the y-axis.</p>

- Fraction of Overlapping-Peak Length

<p align="justify">Fraction of Overlapping-Peaks Length is the ratio of length of overlapped peaks between replicates to the total length of peaks in individual sample. This metric reflects consistency between replicate samples. The higher the value, the higher the consistency.</p>

## Installation


### Install the python3 and dependent python packages
- python3
- scipy
- numpy
- pandas
- statsmodels

The python3 and all the dependent python packages above are included in anaconda3. So we strongly recommend the installation of anaconda3.



#### Download the anaconda3


```
wget https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86.sh
```


#### Install anaconda3

```
bash Anaconda3-5.2.0-Linux-x86.sh -p write-permission-directory/anaconda3
```

#### Add anaconda3 to environment variable

```
export PATH=complete_path_to_anaconda3/bin:$PATH
```

#### Check it

```
which python
```
If successful, it will return similar result
```
/public/work/guoshi/bin/anaconda3/bin/python
```
### Install other dependent tools
- samtools >= 1.8
- bedtools >= 2.27

If samtools and bedtools are not installed on your Linux system, installing them by conda is Recommended.
First, add the bioconda channel as well as the other channels bioconda depends on:

```
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
```

Second, run the install command:
```
conda install samtools
conda install bedtools
```

## Install metqc

First, clone:
```
git clone https://github.com/Epigenomics-Lab/metaqc.git
```

Then install:
```
cd metaqc
pip install .
```

### Check the installation

```
metaqc -h
```

## Usage


List all the options
 
```
metaqc -h
```



#### Run metaqc using 2 sample replicates to test:

* The samples for testing can be downloaded from http://epigenome.sysu.edu.cn/m6A/download


* Single end sequencing
```
metaqc -p IP_1.bam,IP_2.bam -u input_1.bam,input_2.bam -t SE -s hg19 -g genes.gtf -o metaqc_test_SE
```

* Paired end sequencing
```
metaqc -p IP_1.bam,IP_2.bam -u input_1.bam,input_2.bam -t PE -s hg19 -g genes.gtf -o metaqc_test_PE
```

If you have 3 sample Replicates, use comma to separate sample replicates. Note: There is no space between commas.

## Uninstall metaqc

```
pip uninstall metaqc
```

