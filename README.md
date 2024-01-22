# Bachelor Thesis - Android Application Analysis with Machine Learning Transformers

## Overview

This repository contains a tool developed for analyzing Android applications using a machine learning pipeline based on transformers. The primary focus is on summarizing source code and classes within Android applications. The tool is designed with two models: CodeT5 for summarizing source code and T5 for summarizing classes. The project utilizes the Jadx decompiler to obtain the source code of Android applications and provides a web interface using the Python Dash framework.


**Note: The tool's ability to analyze and summarize Android applications can contribute to cybersecurity efforts by providing insights into potential vulnerabilities, code anomalies, and obfuscated elements that may pose security risks.**
## Requirements

Before using the tool, ensure that you have installed the Jadx decompiler. You can find the Jadx decompiler [here](https://github.com/skylot/jadx).

## Installation

To adapt the tool to your machine, follow these steps:

1. Navigate to the "/assets/Decompile.py" file.
2. Update the "jadxPath" variable with the path to your Jadx binary. For example: "C:/[your route]/jadx-1.4.4/bin/jadx".
3. For Linux-based architectures, remove the following content on line 29: "shell=True,". It should look like: "output = subprocess.run(command, capture_output=True, text=True).stdout".

## Abstract

In this final degree project, we present a machine learning tool designed to ease the analysis of Android applications. Leveraging the Transformer architecture, specifically CodeT5 and T5 models, the tool summarizes source code and classes within Android applications. The source code is obtained using the Jadx decompiler, and the tool is accessible through a web interface built with the Python Dash framework.

Aside from the tool's development, the thesis offers an in-depth exploration of the Transformer architecture and its relevance in sequence modeling. It also provides a comprehensive review of key Transformer models in the context of source code and natural language processing. Furthermore, the thesis outlines essential characteristics of the Android platform on which the analyzed applications run.

In summary, while the tool demonstrates promise for analyzing and summarizing Android applications, it faces challenges in comprehending obfuscated elements resulting from application decompilation. With the implementation of improved strategies, the tool holds significant potential for future applications.
