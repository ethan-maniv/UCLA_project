from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import math
import re
from collections import Counter
import os
import xlrd
from flask import Flask


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']

        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        q5 = request.form['q5']
        q6 = request.form['q6']
        q7 = request.form['q7']
        
        v2 = gender + " " + q1 + " " + q2 + " " + q3 + " " + q4 + " " + q5 + " " + q6 + " " + q7
        
        WORD = re.compile(r"\w+")
        def text_to_vector(text):
            words = WORD.findall(text)
            return Counter(words)
        def get_cosine(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum([vec1[x] * vec2[x] for x in intersection])

            sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
            sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)

            if not denominator:
                return 0.0
            else:
                return float(numerator) / denominator

        df = pd.read_excel('ucladata2.xlsx')
        df.shape
        columns = ['Gender', 'q1', 'q2', 'q3','q4','q5','q6','q7', 'Insta', 'Snap']
        df[columns].head(5)

        def get_important_features(data):
            important_features = []
            for i in range(0, data.shape[0]):
                important_features.append(str(data['Gender'][i]) + ' '+str(data['q1'][i])+' ' + str(data['q2'][i])+ ' ' + str(data['q3'][i]) +  ' ' + str(data['q4'][i])
                                          +  ' ' + str(data['q5'][i]) +  ' ' + str(data['q6'][i])+ ' ' + str(data['q7'][i]))

            return important_features
        
        df['important_features'] = get_important_features(df)


        def final(word):
            size = df.size/7
            size = int(size)
            vec1 = text_to_vector(v2)
            max = 0
            index = 0
            for i in range(4):
                vector2 = text_to_vector(df['important_features'][i])
                cosine = get_cosine(vec1, vector2)
                #print(cosine)
                if(cosine>max):
                    max = cosine
                    index = i
            max = "{:.2f}".format(max*100)
            return "" + df['Name'][index] + " is the best roomate for you" + " "+"\nYou guys have a similarity score of:" + " " + str(max) + "%\n" + "\n" + "Their social medias are" +" " "Instagram:@ " + df['Insta'][index] + " " +"Snapchat:@ " + df['Snap'][index] 
            


        return final(v2)
        
    
    return render_template('form.html')




if __name__ == '__main__':
    app.run(debug=True)
