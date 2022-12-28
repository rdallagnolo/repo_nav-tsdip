import os
import streamlit as st

st.header("All profiles")

new_dip = st.button("add new dip")


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
        from pathlib import Path

        path = Path(trg)

        for f in path.iterdir():
            if f.is_file() and f.suffix in ['.txt']:
                f.rename(f.with_suffix('.py'))
    
    else:
        st.write("nothing new to plot")