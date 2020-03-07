# Agoda Assignment

Program that can be used to download data from multiple sources and protocols to local disk. 
The list of sources will be given as input in the form of urls (e.g. http://my.file.com/file, ftp://other.file.com/other, sftp://and.also.this/ending etc). 
The program download all the sources, to a configurable location (file name should be uniquely determined from the url) and then exit. 
considerations:
 - The program should extensible to support different protocols
 - Some sources might very big (more than memory)
 - Some sources might be very slow, while others might be fast
 - Some sources might fail in the middle of download, we never want to have partial data in the final location.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
 - python 3 (3 or 3plus version)

## Installing

```
git clone https://github.com/fartashh/Agoda_Test_Downloader
```

## Database creation

```
for databse copy content of file (config.sql) to workbench
or mysql command line.

```

## Configurations

```
For Databse configuration use the default configurations which will create after running the 
config.sql file or you can change in "config.ini" file

    SERVER_ADDR    = 127.0.0.1      (x.x.x.x)
    SERVER_USER    = agoda          (user name)
    SERVER_PASS    = Snx@D3fault    (pasword)
    DATABASE       = download       (database name)

For Download File location:

    download_location = /Agoda_Test_Downloader/downloads  (Any location e.g: /user/xyyz/download)

To change configurations of below changes are requires in "config.ini" file.

 - For big data(more than memory) update value of below variable: 
        max_size = 655360  (in bytes)
 - For source speed(fast/slow) update value of below variable:
        max_time = 30 (in sec)
 
```

## Running the Downloader

Download one file
```
python download.py -u https://github.com/CaliDog/certstream-python.git 
```
Download more than one file
```
python download.py -u https://github.com/CaliDog/certstream-python.git ftp://ftp.is.co.za/pub/squid/squid-3.1.23.tar.gz 
```
## Running the tests

```
python test_download.py  
```



