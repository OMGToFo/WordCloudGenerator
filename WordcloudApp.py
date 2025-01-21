import pandas as pd
import streamlit as st

from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from wordcloud import WordCloud
import matplotlib.pyplot as plt


import random # for word cloud color schemas

st.header('Word Cloud Generator')

st.subheader("")

st.subheader("Upload Excelfile with Textcolumns to be analyzed:")
uploaded_file1 = st.file_uploader("Upload Excel-File", type=["xlsx", "xls", "xlsm"])

if uploaded_file1:
    dfAntworten = pd.read_excel(uploaded_file1)

    originalTabellenexpander = st.expander("Original Rawdata:")
    with originalTabellenexpander:
        st.dataframe(dfAntworten)

    st.subheader("")
    st.markdown("---")
    st.write("")

    st.info("Choose a ID-Variable/Column - oft helpful wenn merging datasets afterwards")
    IDvariablelAuswahl = st.selectbox("Choose ID-Variable/column:", dfAntworten.columns)
    dfAntworten['ID'] = dfAntworten[IDvariablelAuswahl]



    dfAntwortenNurText = dfAntworten.select_dtypes(include=[object])

    st.info("Text-Variable/Column")
    variablelAuswahl = st.selectbox("Choose a Text-Variable/Column to be analyzed:", dfAntwortenNurText.columns)
    dfAntworten['offeneAntworten'] = dfAntworten[variablelAuswahl]

    dfAntworten["offeneAntworten"] = dfAntworten["offeneAntworten"].values.astype(str)

    erstBuchstabenCapitalize = st.checkbox("Erste Buchstaben anfangs Satz gross? Hilft ev Wortzählung und Wordcloud")
    if erstBuchstabenCapitalize:
        dfAntworten["offeneAntworten"] = dfAntworten["offeneAntworten"].str.capitalize()

    erstBuchstabenGross = st.checkbox("Alle erste Buchstabengross? Hilft ev Wortzählung und Wordcloud")
    if erstBuchstabenGross:
        dfAntworten["offeneAntworten"] = dfAntworten["offeneAntworten"].str.title()

    st.write(dfAntworten["offeneAntworten"])



    countWords = st.checkbox("Count Words?")
    if countWords:
        from collections import Counter

        result = Counter(" ".join(dfAntworten['offeneAntworten'].values.tolist()).split(" ")).items()
        result = dict(result)

        data = [{'Wort': key, 'Anzahl': value} for key, value in result.items()]
        result_df = pd.DataFrame(data)
        result_df = result_df.sort_values(by='Anzahl', ascending=False)

        st.sidebar.dataframe(result_df)

        if len(result_df) > 10:
            wordCloudStart = st.checkbox("Generate Wordcloud?")
            if wordCloudStart:
                excluded_words = st.text_input("Enter words to exclude from Wordcloud (comma-separated):", value="Nicht,nicht,Nichts,nichts,und,die,der,das, nan,Rien,rien,Die,Der,Das,et,ist,est,Les,mit,Le,La,le,la,Nan,Und,Ist,Et")
                excluded_words = [word.strip() for word in excluded_words.split(',')]
                st.sidebar.write("Bereinigtes Dataframe:")
                
                # Filter out excluded words
                bereinigtes_dataframe = result_df[~result_df['Wort'].isin(excluded_words)]
                
                # Ensure 'Wort' column contains only valid strings
                bereinigtes_dataframe = bereinigtes_dataframe.dropna(subset=['Wort'])
                bereinigtes_dataframe['Wort'] = bereinigtes_dataframe['Wort'].astype(str).str.strip()
                bereinigtes_dataframe = bereinigtes_dataframe[bereinigtes_dataframe['Wort'] != '']

                st.sidebar.write(bereinigtes_dataframe)

                # Create a dictionary for word frequencies
                frequencies = dict(zip(bereinigtes_dataframe['Wort'], bereinigtes_dataframe['Anzahl']))

                # Allow user to select a color scheme
                color_scheme = st.selectbox(
                    "Select a color scheme for the WordCloud:",
                    ["Default", "Grayscale", "Warm Colors", "Cool Colors", "Random Colors"]
                )

                import random

                def grayscale_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                    random_state = random_state or random
                    return f"hsl(0, 0%, {random_state.randint(40, 100)}%)"

                def warm_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                    random_state = random_state or random
                    return f"hsl({random_state.randint(0, 50)}, 100%, 50%)"

                def cool_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                    random_state = random_state or random
                    return f"hsl({random_state.randint(180, 270)}, 100%, 50%)"

                def random_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                    random_state = random_state or random
                    return f"hsl({random_state.randint(0, 360)}, 100%, 50%)"




                # Generate the word cloud using the dictionary
                wordcloud = WordCloud(width=800, height=400).generate_from_frequencies(frequencies)


                # Apply the selected color scheme
                if color_scheme == "Grayscale":
                    wordcloud = wordcloud.recolor(color_func=grayscale_color_func)
                elif color_scheme == "Warm Colors":
                    wordcloud = wordcloud.recolor(color_func=warm_color_func)
                elif color_scheme == "Cool Colors":
                    wordcloud = wordcloud.recolor(color_func=cool_color_func)
                elif color_scheme == "Random Colors":
                    wordcloud = wordcloud.recolor(color_func=random_color_func)





                # Display the word cloud
                _=""" alte Schreibweise
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis("off")
                """

                # Create a figure and axis for the WordCloud
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")  # Turn off axes for WordCloud



                st.pyplot()
