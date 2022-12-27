import os
import re
import sys
import csv
import threading
import subprocess

from transformers import RobertaTokenizer, T5ForConditionalGeneration
import torch

from Utils import logTheProgress
### Util methods ###

def isAMethodHeader(line):
    if re.search(r".*@Override.*", line):# means: * then "@Override" then *
        return True, True
    elif re.search(r".+\(.*\).*\{$", line):# means: * then "("  * then ")" * then "{" --.+\(.*\).*\{.*[^}][^;].+\(.*\).*\{
        return True, False
    else:
        return False, False

def checkBrackets(line, bracket_counter):
    isMethod=True
    if re.search(r".*{$", line):#means: end line with "{"
        bracket_counter+=1
    if re.search(r"^[\s]*}", line):#means: start line with "}" (ignoring whitespaces)
        bracket_counter-=1
    if bracket_counter==0:
        isMethod=False
    return bracket_counter,  isMethod

def cleanMethod(method):
    return method.replace('\n','')

def removeRepetitiveWords(text):
  words = text.split()
  result = []
  for i in range(len(words)):
    if i == 0 or words[i] != words[i-1]:
      result.append(words[i])
  return ' '.join(result)

def initializeDataFile(apkName):
    header = ["Path", "Method", "Summary"]
    with open(os.getcwd()+"/UploadedAPKs/"+apkName+'.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    f.close()

def saveToFile(data, apkName):
    with open(os.getcwd()+"/UploadedAPKs/"+apkName+'.csv', 'a+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    f.close()

##### Core functionality ####

def extractMethod(javaclass, line, hasOverride):
    isMethod = True
    method , shortedStrings = "", ""
    if hasOverride:
        method+=line
        line = javaclass.readline()
    method+=line
    bracket_counter=1
    while isMethod:
        line = javaclass.readline()
        if len(line)>250:
            shortedStrings += "This line has been shortened keeping the first 25 characters" + line
            line =  line[0:25] + '"#LONG DECLARATION ' * 3
        method += line
        bracket_counter, isMethod = checkBrackets(line, bracket_counter)
    return  method, shortedStrings

def codeT5(method):
    inputs_dict = tokenizer(method, return_tensors="pt")
    input_ids = inputs_dict.input_ids.to(device)
    generated_ids = model.generate(input_ids, max_length=20)
    return tokenizer.decode(generated_ids[0], skip_special_tokens=True)

def extractMethods(pathToFile,apkName, counter):
    nameClass, methods, methodsSummariezed = [], [], []
    with open(pathToFile, mode='r', encoding='utf-8') as javaclass: 
        line=javaclass.readline()
        while line:
            isMethod, hasOverride = isAMethodHeader(line)
            if isMethod:
                counter+=1
                method, shortedStrings = extractMethod(javaclass, line, hasOverride)
                index = pathToFile.find("sources")
                nameClass.append(pathToFile[index+8:])
                if len(cleanMethod(method))>2000:
                    methods.append("This method has been shortened to the first 2000 characters \n"+ shortedStrings +method)
                    methodsSummariezed.append(removeRepetitiveWords(codeT5(cleanMethod(method[0:2000]))))
                else:
                    methods.append(shortedStrings + method)
                    methodsSummariezed.append(removeRepetitiveWords(codeT5(cleanMethod(method))))
            line=javaclass.readline()
    javaclass.close()
    saveToFile(list(zip(nameClass, methods, methodsSummariezed)), apkName)
    return counter    

def getAllFiles(directory, apkName, totalMethods, counter=0):
    listdirectory=os.listdir(directory)
    for element in listdirectory:
        path = os.path.join(directory, element)
        if os.path.isdir(path):
            counter=getAllFiles(path, apkName, totalMethods, counter)
        elif os.path.isfile(path):
            counter=extractMethods(path, apkName, counter)
        logTheProgress(counter, totalMethods, "Code")
    return counter

if __name__ == "__main__":
    apkName = sys.argv[1]
    totalMethods = sys.argv[2]

    apkName, extension = os.path.splitext(apkName)
    directory = os.getcwd().replace(os.sep, '/')+"/UploadedAPKs/decompiledAPK/sources"
    initializeDataFile(apkName)
    
    device = 0 if torch.cuda.is_available() else "cpu"
    print("Using device: {}".format(device))
    if device != "cpu":
        torch.backends.cudnn.benchmark = True
    model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')
    tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base')
    model.to(device)

    getAllFiles(directory, apkName, totalMethods)
    logTheProgress("Done",0, "Code")

    thread = threading.Thread(target=subprocess.call(['python', "./assets/T5.py", apkName], shell=True))
    thread.start()