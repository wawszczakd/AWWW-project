# AWWW Project

## Overview

This project is a web application developed as a part of a "Aplikacje WWW" (WWW
Applications) course project. The goal of the project is to create a user
interface for the SDCC compiler.

### Features

- Account creation: Users can create accounts to access the application.
- Folder management: Users can create folders and upload C files.
- Compilation: Users can compile uploaded C files with various compiler options.
- Assembly display: The application displays the compiled assembly files.
- File sections: Users can create sections within files.

## Usage

### Installation

```shell
git clone git@github.com:wawszczakd/AWWW-project.git
cd IO-project
```

Django 4.0 is required. It is recommended to set up a virtual environment before
installing the project's dependencies.

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

###Running the Project

To run the project, use the following command:

```shell
python3 manage.py runserver
```

This command starts the development server, allowing you to access the project
in your web browser.
