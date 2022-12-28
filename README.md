# In-sea sound velocity dashboard

Displaying TSDip profiles with python, plotly and streamlit in a dashboard.

## General guideline

Sound velocity profiles have to be exported in the MiniSoft SD200W software as a list using `tab` as a the delimiter and `DOS` as file type. That will create a `.prn` file. Rename the file to the name you want to display in the dashboard. Try to follow some sort of logic structure as `TSDip-1.txt` or equivalent.

> **Warning**
> Replace the `.prn` with a `txt`.  

## File structure

The following file structure and naming convention have to be used in order to get the dashboard to work:

```
tsdip
    |   tsdip_app.py
    |   code_template.py
└───data
└───pages
    
```

Under the main project folder, here named `tsdip`, two python files are saved:

> **Note**
> tsdip_app.py: the main code file that will be run by `streamlit run`

> **Note**
> code_template.py: used by the main code file containing the code for dataframe manipulation and graphs contructions 

> **Note**
> data: is a folder where the `TSDip-n.txt`files have to be saved

> **Note**
> pages: is a folder where the streamlit pages will be stored