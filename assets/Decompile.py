import subprocess
import os

def getNumberOfMethods():
    with open('./UploadedAPKs/JadxOutput.log', 'r') as f:
        output = f.read()
    f.close()
    posStart = output.find(", methods: ")+11
    posEnd = output.find(", instructions: ")
    numMethods=output[posStart:posEnd]
    if numMethods.isdigit():
        numMethods = int(numMethods)
    else:
        print("Error reading JADX output file")
    return numMethods

def decompileAPK(apkName):
    # add shell=True for Windows architectures
    jadxPath = "Z:/7o_Semestre_Universidad/TFG/jadx-1.4.4/bin/jadx"
    apkPath = os.path.join("./UploadedAPKs" , apkName).replace(os.sep, '/')
    command = [
        jadxPath,
        "-d", "./UploadedAPKs/decompiledAPK",
        "--comments-level", "none",
        "--deobf",
        "--log-level", "info",
         apkPath,
    ]
    output = subprocess.run(command, shell=True, capture_output=True,  text=True).stdout
    with open('./UploadedAPKs/JadxOutput.log', 'w') as f:
        f.write(output)
    f.close()

