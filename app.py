from flask import Flask, render_template, request, url_for
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

def undergrad(url_string):
    current_page = 1
    data = []
    proceed = True
    firstloop = True
    while proceed:
        if firstloop:
            url = url_string
            firstloop = False
        else:
            url = url_string + str(current_page) + "/"
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        if soup.title.text == "404 - Wits University":
            proceed = False
        else:
            all_books = soup.find_all("a", class_="search-result")
            for book in all_books:
                item = {
                    'Title': book.find("h3").text.strip(),
                    'Details': book.find("div", class_="details").text.strip(),
                    'Description': book.find("div", class_="description").text.strip()
                }
                data.append(item)
        current_page += 1

    return data

#@app.route('/')
#def index():
#    return render_template('indexx.html')
@app.route('/')
def home():
    return render_template('landingPage.html')

@app.route('/wits')
def wits():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    faculty = request.form['faculty']
    url_mapping = {
        "Science": "https://www.wits.ac.za/undergraduate/academic-programmes/faculty-of-science/",
        "Health Science": "https://www.wits.ac.za/undergraduate/academic-programmes/faculty-of-health-sciences/",
        "Engineering": "https://www.wits.ac.za/undergraduate/academic-programmes/faculty-of-engineering-and-the-built-environment/",
        "Commerce, Law & Management": "https://www.wits.ac.za/undergraduate/academic-programmes/faculty-of-commerce-law-and-management/",
        "Humanities": "https://www.wits.ac.za/undergraduate/academic-programmes/faculty-of-humanities/"
    }
    if faculty in url_mapping:
        data = undergrad(url_mapping[faculty])
    else:
        data = []
    
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
