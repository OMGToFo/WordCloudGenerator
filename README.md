# WordCloudGenerator

Simple WordCloud Generator
Welcome to the Simple WordCloud Generator, a user-friendly Streamlit app that enables you to create customized WordClouds from your text data with just a few clicks. 🎨✨

App Features
Upload and Analyze Text Data: Upload Excel files and select columns for text analysis.
Word Frequency Count: Automatically count word frequencies, with the option to exclude unwanted words.

Customizable WordClouds:
Configure font size range, background color, contour color, and width.
Limit the number of words displayed in the WordCloud.
Choose from multiple color schemes (default, grayscale, warm colors, cool colors, random colors).
Use an image mask to define the shape of your WordCloud.

Export Options: View and export cleaned datasets used to generate WordClouds.

Live Demo
Check out the live app here:
👉 Simple WordCloud Generator
https://simplewordcloudgenerator.streamlit.app/

How to Use
Upload Your Data: Upload an Excel file containing text data. The app supports .xlsx, .xls, and .xlsm file formats.
Select a Text Column: Choose the column from your dataset containing the text to be analyzed.
Configure Your WordCloud:
Exclude specific words by entering them in the "Excluded Words" field.
Adjust font size, background color, and other settings.
Optionally, upload an image mask to customize the WordCloud shape.
Generate and Download: Generate your WordCloud and download the cleaned dataset for further analysis.
Tech Stack
Frontend: Streamlit for an intuitive and interactive user interface.
Backend:
Pandas for data manipulation.
WordCloud for generating WordClouds.
Langdetect for language detection.
Visualization: Matplotlib for rendering the WordClouds.
Local Installation
To run the app locally:

Clone this repository:

git clone https://github.com/your-username/simple-wordcloud-generator.git
cd simple-wordcloud-generator
Install dependencies:


pip install -r requirements.txt

Run the app:
streamlit run app.py

Open the app in your browser at http://localhost:8501.

Folder Structure
.
├── app.py                 # Main application script
├── requirements.txt       # Dependencies
└── README.md              # Project documentation

Contributing
We welcome contributions! Feel free to submit a pull request or report issues.
