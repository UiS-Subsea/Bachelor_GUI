# Bachelor_GUI

Repo for alle koselige gutter i GUI seksjonen i UiS-Subsea

# Måten prosjektet skal bli såtte opp

GUI python fil som impoerterer ei UI fil fra QT Designer

# Venv

Husk å ta select interpreter og bytt til python 3.9

Powershell:
python -m venv venv
venv\Scripts\Activate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# Requirements !

pip install -r requirements.txt

for å oppdatere requirements om du he installert ei ny python pakke i virtual environment (venv)

pip freeze > requirements.txt

# Formatering av filer

black {source_file_or_directory}

eksempel:
black D:\Bachelor_GUI

mest sannsynlig berre å bytte ut D med C p diskane dokka <3
