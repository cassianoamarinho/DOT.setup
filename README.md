<h1 align="center">DOT.setup</h1>

*<p align="center">A project to setup my workspace.</p>*

## About

Use the `DOT.setup` to backup, restore and install initial programs and files.

### Features:

- Backup dot files in local machine to this repository.

- Restore dot files in this repository to local machine.

- Initial setup and installation packages and configurations.

- Generate an encryption key for the sensive files.

## Installation

### Requirements:

- [Python](https://python.org/) version 3.6.15 (or above)

### How to install:

- Run: 

  ```
  $ git clone https://github.com/cassianoamarinho/DOT.setup.git ~/.dot.setup
  ```

## Usage

### Options:

```
$ python ~/.dot.setup/setthefuckup.py -h
usage: setthefuckup.py [-h] [-n] command

positional arguments:
  command       options: install, restore, backup, keygen or status.

options:
  -h, --help         show this help message and exit
  -n, --notlog       not show logs
  -c, --cryptofiles  enabled the backup of sensive files
```

### Examples:

#### Backup dot files whitout console log:

```
$ python ~/.dot.setup/setthefuckup.py backup -n
```

#### Backup dot files with crypto.key:

```
$ python ~/.dot.setup/setthefuckup.py backup -c
```

#### Generate a crypto.key:

```
$ python ~/.dot.setup/setthefuckup.py keygen
```

#### view the modified dot files:

```
$ python ~/.dot.setup/setthefuckup.py status
```

## Credits

_this script was born when i'm high on the carnival holiday.