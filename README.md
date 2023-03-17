# Bachelor_GUI

Repo for alle koselige gutter i GUI seksjonen i UiS-Subsea

# Viktige ting om installasjon

QT Designer
Python 3.9

pip install PyQt6
pip install PyQt6-tools

# Formatering av filer

black {source_file_or_directory}

eksempel:
black D:\Bachelor_GUI

mest sannsynlig berre å bytte ut D med C p diskane dokka <3

# Måten prosjektet skal bli såtte opp

GUI python fil som impoerterer ei UI fil fra QT Designer

# Requirements !

pip install -r requirements.txt

for å oppdatere requirements om du he installert ei ny python pakke i virtual environment (venv)

pip freeze > requirements.txt

# Venv

Powershell:
venv\Scripts\Activate

Mac/Linux:
source venv/bin/activate


# Mac

For å endre venv versjon:
virtualenv -p /path/to/python3.9.6 venv
Brukte:
pip install virtualenv
virtualenv -p /usr/bin/python3 venv