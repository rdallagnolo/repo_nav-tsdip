import os
import streamlit as st
st.set_page_config(layout="wide")

new_dip = st.sidebar.button("add new dip")

if new_dip == True:

    # libraries to be used
    from pathlib import Path
    import shutil
    import os
    
    # defining source and destination
    # paths
    src = '/home/rod/Documents/DataScience/my_projects/tsdip/data/'
    trg = '/home/rod/Documents/DataScience/my_projects/tsdip/pages/'

    # list of files in the data and page folder
    data_files = os.listdir(src)
    page_files = os.listdir(trg)

    # check for new tsdip
    if len(data_files) > len(page_files):

        # lists of all files in the src and trg directory
        files=os.listdir(src)
        pages=os.listdir(trg)                          


        # renaming itens in files list so we can compare against 
        files_pythonic = []
        for i in files:
            files_pythonic.append(i[0:7] + '.py')

        new_dips = list(set(files_pythonic) - set(pages))
        new_dips_text = []
        for i in new_dips:
            new_dips_text.append(i[0:7] + '.txt')




        # iterating over all the files in
        # the source directory
        for fname in new_dips_text:

            # copying the files to the
            # destination directory
            shutil.copy2(os.path.join(src,fname), trg)

        #### replacing file contents with template
        from shutil import copyfile

        source = '/home/rod/Documents/DataScience/my_projects/tsdip/code_template.py'
        
        for fname in new_dips_text:
            copyfile(source,f'/home/rod/Documents/DataScience/my_projects/tsdip/pages/{fname}')

        ## adding file name as target

        #files=os.listdir(trg)
        os.chdir(trg)

        for i in new_dips_text:

            # creating a variable and storing the text
            # that we want to search
            search_text = "target-name"

            # creating a variable and storing the text
            # that we want to add
            replace_text = i

            # Opening our text file in read only
            # mode using the open() function
            with open(i, 'r') as file:

                # Reading the content of the file
                # using the read() function and storing
                # them in a new variable
                data = file.read()

                # Searching and replacing the text
                # using the replace() function
                data = data.replace(search_text, replace_text)

            # Opening our text file in write only
            # mode to write the replaced content
            with open(i, 'w') as file:

                # Writing the replaced data in our
                # text file
                file.write(data)       
        
        
        
        ##### ​change the file name
        path = Path(trg)

        for f in path.iterdir():
            if f.is_file() and f.suffix in ['.txt']:
                f.rename(f.with_suffix('.py'))
    
        
    else:
        st.sidebar.write("nothing new to plot")


#### creating all profiles graph
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

f = Path('/home/rod/Documents/DataScience/my_projects/tsdip/home_files')

if len(os.listdir(f)) == 0:
    print(" ")
else:
    
    fig1 = go.Figure()

    for csv in f.glob("*.csv"):
        fig1.add_traces(
            px.line(pd.read_csv(csv), x="SoS", y="Depth")
            .update_traces(line_color=None, showlegend=True, name=csv.name[0:7])
            .data
        )
        
    fig1.update_yaxes(autorange="reversed")

    fig1.update_layout(
        xaxis={'side':'top'},
        xaxis_title="Speed of sound (m/s)",
        yaxis_title="Depth (m)",
        template='ggplot2',
        height=800,
        width=600)

    # survey polygon
    df = pd.read_csv(f"/home/rod/Documents/DataScience/my_projects/tsdip/survey_polygon.txt",sep="\t")
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=df['Easting'], y=df['Northing'],
                        mode='lines',
                        name='Survey Polygon'))
    fig2.update_layout(
        xaxis_title="Easting (m)",
        yaxis_title="Northing (m)",
        legend_title="Dips",
        height=800,
        width=600,
        template='plotly_white')


    col1, col2 = st.columns(2)

    with col1:
        st.text('All profiles')
        st.plotly_chart(fig1)
    
    with col2:
        st.text('Survey polygon')
        st.plotly_chart(fig2)
        

        
