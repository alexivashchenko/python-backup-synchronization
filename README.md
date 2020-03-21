# python-backup-synchronization


## Description

Simple Python script to synchronize folders between your server and your local pc.

The main purpose of the script is to create the "mirror" of the daily server backups on your local machine.

One-way synchronization "Server Folder -> Local Folder".

You can synchronize multiple directories.

You can schedule the script to run daily on your pc.

The script:
* Compares the Server folder and the Local folder
* Download new files from the Server folder
* Remove old files from the Local folder


## Usage

1. Create your `config.py` file from `config-sample.py`.
2. Run `py ftp.py` from Command Line


