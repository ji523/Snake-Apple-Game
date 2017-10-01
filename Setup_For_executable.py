import cx_Freeze

executables = [cx_Freeze.Executable("The Snakey Cakey.py")]

cx_Freeze.setup(
    name="Slither",
    options={"build.exe":{"packages":["pygame"],"include_files":["apple.png","arena.png","body.png","icon.png","snakehead.png","tailleft.png","tailright.png","Crash.png","music.png"]}},

    description = "The Snakey Cakey",
    executables=executables
    
    )
