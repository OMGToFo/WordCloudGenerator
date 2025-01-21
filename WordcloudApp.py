import pandas as pd
import streamlit as st

from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from wordcloud import WordCloud
import matplotlib.pyplot as plt


import random # for word cloud color schemas


from PIL import Image
import numpy as np

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

                
                # Filter out excluded words
                bereinigtes_dataframe = result_df[~result_df['Wort'].isin(excluded_words)]
                
                # Ensure 'Wort' column contains only valid strings
                bereinigtes_dataframe = bereinigtes_dataframe.dropna(subset=['Wort'])
                bereinigtes_dataframe['Wort'] = bereinigtes_dataframe['Wort'].astype(str).str.strip()
                bereinigtes_dataframe = bereinigtes_dataframe[bereinigtes_dataframe['Wort'] != '']

                st.sidebar.success("Bereinigtes Dataframe:")
                st.sidebar.write(bereinigtes_dataframe)

                # Create a dictionary for word frequencies
                frequencies = dict(zip(bereinigtes_dataframe['Wort'], bereinigtes_dataframe['Anzahl']))


                # WordCloud Configuration Options
                st.sidebar.header("WordCloud Configuration")
                max_words = st.sidebar.slider("Maximum Number of Words", min_value=10, max_value=500, value=200, step=10)
                font_size = st.sidebar.slider("Font Size Range", min_value=10, max_value=100, value=(10, 50))
                background_color = st.sidebar.color_picker("Background Color", value="#ffffff")
                contour_color = st.sidebar.color_picker("Contour Color", value="#000000")
                contour_width = st.sidebar.slider("Contour Width", min_value=0, max_value=10, value=1)

                # Option to Upload Mask for WordCloud Shape
                uploaded_mask = st.sidebar.file_uploader("Upload Mask Image (Optional)", type=["png", "jpg", "jpeg"])
                mask = None
                if uploaded_mask:
                    mask_image = Image.open(uploaded_mask).convert("L")
                    mask = np.array(mask_image)



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





                # Generate the WordCloud
                wordcloud = WordCloud(
                    width=800,
                    height=400,
                    max_words=max_words,
                    min_font_size=font_size[0],
                    max_font_size=font_size[1],
                    background_color=background_color,
                    contour_color=contour_color,
                    contour_width=contour_width,
                    mask=mask
                ).generate_from_frequencies(frequencies)




                # Apply the selected color scheme
                if color_scheme == "Grayscale":
                    wordcloud = wordcloud.recolor(color_func=grayscale_color_func)
                elif color_scheme == "Warm Colors":
                    wordcloud = wordcloud.recolor(color_func=warm_color_func)
                elif color_scheme == "Cool Colors":
                    wordcloud = wordcloud.recolor(color_func=cool_color_func)
                elif color_scheme == "Random Colors":
                    wordcloud = wordcloud.recolor(color_func=random_color_func)




                # Create a figure and axis for the WordCloud
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")  # Turn off axes for WordCloud



                st.pyplot(fig)
