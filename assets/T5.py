
from transformers import pipeline
import pandas as pd
import os
import sys
import torch

from transformers import T5Tokenizer
from Utils import logTheProgress
def countSlashes(path):
    return path.count('\\')

def joinSummaries(df):
    dfJoined, lengths = [], []
    for i in range(len(df)):
        joined=""
        for s in df[i]:
            joined+=s.replace('\n','')
        dfJoined.append(joined)
        lengths.append(len(joined) )
    return dfJoined, lengths

def splitStringEqualParts(string, num_parts):
  part_length = len(string) // num_parts + 1
  parts = [string[i:i+part_length] for i in range(0, len(string), part_length)]
  return parts

def adaptCSV(df): #antes 30 ahora 59 -> MODIFY extractMethods
    bd = df["Path"].apply(lambda row: os.path.dirname(row))
    return pd.DataFrame(list( zip(df["Path"], bd, df["Method"], df["Summary"]) ), columns=["JavaClass", "BaseDir", "Method", "Summary"])

def tokenize(summaries):
    lengthTokenized=[]
    tokenizer = T5Tokenizer.from_pretrained("t5-large")
    for i in range(len(summaries)):
        summarie = len(tokenizer(summaries[i], return_tensors="pt").input_ids[0])
        lengthTokenized.append(summarie)
    return lengthTokenized

def generateAPKStats(apkName):
    path = os.path.join("./UploadedAPKs",apkName+".csv")
    df = adaptCSV(pd.read_csv(path))
    methodsByClass = pd.DataFrame(df.groupby('JavaClass')["Summary"])# at pos 0 we have the class, at poss 1 the summaries
    classes = methodsByClass[0]
    summariesC, lens = joinSummaries(methodsByClass[1])
    numFolders = methodsByClass[0].apply(lambda row:countSlashes(row)-1)
    lengthTokenized = tokenize(summariesC)
    pd.DataFrame(list(zip(classes, summariesC, df.groupby('JavaClass')["Summary"].count(), lens, lengthTokenized, numFolders)), 
                        columns=["Class", "Summaries", "NumSummaries", "Lengths", "LengthsTokenized", "NumFolders"]
                ).to_csv("./UploadedAPKs/methodsByClass_"+apkName+".csv", index=False)
    
def summarizeClasses(apkName):
    path = "./UploadedAPKs/methodsByClass_"+apkName+".csv"
    methodsByClass = pd.read_csv(path)
    out = []
    for i in range(len(methodsByClass)):
        if methodsByClass["Lengths"][i]>100:
            if methodsByClass["LengthsTokenized"][i]>512:
                summarie = ""
                parts = splitStringEqualParts(methodsByClass["Summaries"][i], len(methodsByClass["Summaries"][i])//512 + 1)
                for part in parts:
                    summarie += list(summarizer(part,min_length=5, max_length=20)[0].values())[0] + " :: "
                summarie = [summarie]
            else:
                summarie = list(summarizer(methodsByClass["Summaries"][i],min_length=5, max_length=20)[0].values())
            out.append(summarie[0])
        else:
            out.append(methodsByClass["Summaries"][i])
        logTheProgress(i, len(methodsByClass))
    logTheProgress("Done", 100)
    classesSummarized = pd.DataFrame(list(zip(methodsByClass["Class"], out)), columns=["Classes", "Summaries"])
    classesSummarized.to_csv("./UploadedAPKs/classesSummarized_"+apkName+".csv",index=False)

if __name__ == "__main__":
    apkName = sys.argv[1]
        
    device = 0 if torch.cuda.is_available() else "cpu"
    print("Using device: {}".format(device))
    if device != "cpu":
        torch.backends.cudnn.benchmark = True
    summarizer = pipeline("summarization", model="t5-large", tokenizer="t5-large", framework="pt", device=device)

    generateAPKStats(apkName)
    summarizeClasses(apkName)

