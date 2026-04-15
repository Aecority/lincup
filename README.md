# Linc Up

## Members
- 33: Arnav Mishra
- 2: Sejal Mudkhedkar
- 15: Mrunmayee Katruwar

## Why?
Although urban planning software already exist, the evaluation of the final plans is still a largely manual process. Linc Up aims to be a tool to aid in this step, so a plan can be brought to reality much quicker.

## Setup
- Ensure you have python installed.
- From the directory you want the app to be run from, run `git clone git@github.com:Aecority/lincup.git`
- Run `cd lincup` to enter the project directory.
- Optionally, create and activate a venv.
- Run `pip install -r requirements.txt` to install dependencies.
- Run the entry point `main.py` in any way. From the terminal that would be `python main.py`

## Usage
- You will see an empty grid on startup.
- The left panel of the GUI will have your tools.
- Start by creating your city bounds. Enter your desired width and height.
- The brush section's dropdown menu can be used to set the background to initialize with.
- Click the apply button.
- There are three main sections to the GUI. Brush, Create Structure, and Remove Structure.
- You can change selected sections by clicking on the square buttons next to their headings. (Marked with `[  ]`)
- The brush allows you to draw terrain with the selected terrain type. The size of the brush square can be changed with the slider
- Note: Only pavement and road are considered for pathfinding.
- With the create structure section selected and your desired structure selected, you can create 4 sided structures by clicking on a starting point, then clicking on another point.
- The remove structure section, as the name implies, can remove strucures when they are clicked on.
- After you've made your city layout, click on the submit button.
- Whenever you hover over any home type structure, the structure's living conditions will be shown.
- Keep in mind, any changes made to the city after pressing submit, will undo evaluation. Press the button again to view updated data.
