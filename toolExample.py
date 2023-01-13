from sys import argv
import webbrowser
from fastapi import Header
import pandas as pd
from fuzzywuzzy import fuzz
import nltk
import gspread
import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import true

print('Your query: ', ' '.join(argv[1:]))
query = ' '.join(argv[1:])

df = pd.read_csv('/home/cynthia/Downloads/Galaxy/galaxy/tools/myTools/workflows.csv')
df.dropna(inplace=True)

w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize_text(text):
    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]

df['text_lemmatized'] = df.Annotation.apply(lemmatize_text)
query = lemmatize_text(query)

def get_ratio(row, query):
    name = row
    name1 = query

    return fuzz.token_set_ratio(name, name1)

df['score'] = df['Annotation'].apply(lambda x: get_ratio(x, query))

df1 = df.sort_values('score',ascending = False).head(5)
df1.to_csv('/home/cynthia/Downloads/Galaxy/galaxy/tools/myTools/output.csv', index=False, header=False)
df1 = df1.iloc[:,0:3]
result = df1.to_html(render_links=True, escape=False)

text_file = open("/home/cynthia/Downloads/Galaxy/galaxy/tools/myTools/index.html", "w")
text_file.write(result)
text_file.close()

print("Follow this link: /home/cynthia/Downloads/Galaxy/galaxy/tools/myTools/index.html")

# q = "I want to create a  workflow for phylogenetic analysis"


# scope = ['https://spreadsheets.google.com/feeds',
#          'https://www.googleapis.com/auth/drive']
# credentials = ServiceAccountCredentials.from_json_keyfile_name(
#     '/home/cynthia/Downloads/Galaxy/galaxy/tools/myTools/jsonFileFromGoogle.json', scope)
# gc = gspread.authorize(credentials)


# spreadsheet_key = '1vH4QTSn6s2fhqbS8WdRBIH5AZfueNp9cq5d3w63JvR4'
# wks_name = 'Master'
# d2g.upload(df1, spreadsheet_key, wks_name, credentials=credentials, row_names=True)