This repository contains a tool for analyzing android applications using a machine learning pipeline based on transformers.

Requirements:
Install the Jadx decompiler, available on https://github.com/skylot/jadx

Installation:

For adapting it to your own machines, go to "/assets/Decompile.py" and change the "jadxPath" variable to your current Jadx bin path.
For example : "C:/[your route]/jadx-1.4.4/bin/jadx"

ONLY FOR Linux-based architectures:
In adition, in the same file, "/assets/Decompile.py", remove the following content on the line 29: "shell=True,". 
It should look like: 
"output = subprocess.run(command, capture_output=True,  text=True).stdout"
