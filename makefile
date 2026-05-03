build:
	cd dev-tools-python \
		&& pyinstaller --onefile --windowed \
			--name "ScriptLauncher" \
			--icon "assets/rocket.ico" \
			--add-data "assets/rocket.png:assets" \
			--hidden-import PIL._tkinter_finder \
			run.py

up:
	cd dev-tools-python \
		&& python run.py