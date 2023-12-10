# Family Court Toolkit

This repository contains tools to allow labelling of family court documents.
It uses latex and python. 

## Problem 

The problem that it proposes a solution for is: 

- Family court documents are often scanned and uploaded as PDFs, which makes them unsearchable.
- There are often document dumps from different sources, which have disparate timelines.
- Adding emails and other documents you can easily reach 1000s of pages. 
- Limited bandwidth of the court and your representation means that you need to have a system to boil down your data, in order have the best chance of an outcome that is consistent with the data, and therefore with the truth, and the child's best interest.


## Gather, label, cite. 

Start by gathering your documents, and filling out your case's document tree. 
An example is given in `examples/labelled/full.tex`, you can use a single doc, or several, like one doc for emails, one for psych evaluation, etc. 
<!-- This is done by translating all your files into `.tex` files.   -->

When you include `header.tex` and label the document using `\lb{key}{snippet}{note}`, then every time you compile `full.tex`, labels will be extracted to a csv table named `full_labels.csv`. 

Using `csv2bib.py` you can convert this into a citation database, which allows you to write concise documents to different parties, built on citations from your case documentation, like `brief.tex`, which outputs [brief.pdf](https://github.com/tilmaerts/fct/files/13627234/brief.pdf). 

- For emails you may use the `eml2tex.py` script to convert your emails into latex sections. 
- For scanned documents you can use the `pdf2tex.py`, which uses OCR (tesseract) to convert your PDFs into latex sections.

<!-- The `header.tex` in this project includes some extra macros, in particular the `\lb{label}{text}{note}` and `\sd{date}`. -->

## Editor setup for labelling in vscode

When using vscode, you may want to include the following keybindings to your `keybindings.json` file.
```json
    {
        "key": "ctrl+L",
        "command": "editor.action.insertSnippet",
        "when": "editorTextFocus && editorLangId == 'latex'",
        "args": {
          "snippet": "\\lb{$1}{${TM_SELECTED_TEXT}}{$2}"
        }
    }
```
Labels the selected text with a label and a note.
```json
    {
        "key": "ctrl+D",
        "command": "editor.action.insertSnippet",
        "when": "editorTextFocus && editorLangId == 'latex'",
        "args": {
          "snippet": "\\sdate{${TM_SELECTED_TEXT}}"
        }
    }
```   
Adds a date in the document, which is used for all labels following it until the next date, format is `DD-MM-YYYY`.

## Create timelines
Another useful tool is a visual timeline of events, there is a `timeline_plotter.py` utility added. 

![tl](https://github.com/tilmaerts/fct/assets/95282593/c236c40b-7fe5-4ac9-b033-0379d848f70a)

