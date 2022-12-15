import streamlit as st

st.header("All profiles")

new_dip = st.button("add new dip")


if new_dip == True:

    #### copy tsdip data files to page folder
    from pathlib import Path
    import shutil
    import os

    # defining source and destination
    # paths
    src = '/home/rod/Documents/DataScience/my_projects/nav/tsdip/data/'
    trg = '/home/rod/Documents/DataScience/my_projects/nav/tsdip/pages/'

    # listing all files in the src directory
    files=os.listdir(src)                          

    # iterating over all the files in
    # the source directory
    for fname in files:

        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(src,fname), trg)

    #### replacing file contents with template
    from shutil import copyfile

    source = '/home/rod/Documents/DataScience/my_projects/nav/tsdip/code_template.py'
    
    for fname in files:
        copyfile(source,f'/home/rod/Documents/DataScience/my_projects/nav/tsdip/pages/{fname}')

    ######################################
    # REPLACE TARGET STRING WITH FILENAME STRING
    
    
    
    
    ##### ​change the file name
    from pathlib import Path

    path = Path(trg)

    for f in path.iterdir():
        if f.is_file() and f.suffix in ['.txt']:
            f.rename(f.with_suffix('.py'))