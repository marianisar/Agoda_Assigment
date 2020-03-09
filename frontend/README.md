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

### Installing

```
git clone https://github.com/marianisar/Agoda_Assigment.git
```

### Prerequisites
 - python 3 (3 or above)
 - Flask
 - Flask-RESTful
 - Flask-MySQL
 - Flask-Cors



## Configurations

```
For Databse configuration use the default configurations which will create after running the 
"backend/config.sql" file or you can change in "frontend/db_config" file

    app.config['MYSQL_DATABASE_USER'] = 'agoda'             (user name)
    app.config['MYSQL_DATABASE_PASSWORD'] = 'Snx@D3fault'   (password)
    app.config['MYSQL_DATABASE_DB'] = 'download'            (databse name)
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'         (host x.x.x.x)
```

## Running the Server

```
python main.py 
```

## Displaying the data

open index.html file




