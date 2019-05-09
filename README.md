# Re:VIEW Preview Tool

Tool to live Preview any Re:VIEW format document

## ToDo

### Required Features

* [x] Displays a preview of the specified Re:VIEW document.
* [x] To follow the changes in the re file.
* [x] Do not reset the position of the scroll when the re file is recompiled.
* [x] Do not update the preview when a compile error occurs.
* [x] Compile to EXE format with Pyinstaller.

### If you have time

* [x] Allow the directory to be changed on the GUI.
* [ ] Non-HTML preview (PDF?) also corresponds to.
* [ ] Synchronize to the visual Studio code display line (may be impossible).

## Building the development environment

1. Install Re:VIEW with the `gem install review` command.
2. Run `pipenv install`.
3. Run `npm install`.
4. Run `pipenv run setup`.
5. Enjoy.

## How to Run

1. Make the project root folder the current directory.
2. Enter the pipenv shell with the `pipenv shell` command.
3. Run main.py with the `python ./src/main.py` command

## How to create an executable file

### For Windows

1. Make the project root folder the current directory.
2. Enter the pipenv shell with the `pipenv shell` command.
3. Execute `./create_exe.ps1`.