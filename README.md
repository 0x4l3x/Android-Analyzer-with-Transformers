<h1>This repository contains a tool for analyzing android applications using a machine learning pipeline based on transformers.</h1>

<h1>Requirements:</h1>

Install the Jadx decompiler, available on https://github.com/skylot/jadx

<h1>Installation:</h1>

For adapting it to your own machines, go to "/assets/Decompile.py" and change the "jadxPath" variable to your current Jadx bin path.
i.e. "C:/[your route]/jadx-1.4.4/bin/jadx"

<h1>ONLY on Linux-based architectures:</h1>

In adition, in the same file, "/assets/Decompile.py", remove the following content on the line 29: "shell=True,". 

It should look like: 

"output = subprocess.run(command, capture_output=True,  text=True).stdout"
