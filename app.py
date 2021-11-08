from flask import Flask, render_template, send_file, request, session, redirect, url_for, sessions, flash
from main import *
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup


app = Flask(__name__)
app.secret_key = "hello"

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == "POST":
        url = request.form['url']
        keyword = request.form['keyword']
        try:
            req = Request(url, headers = {'User-Agent': 'Mozilla/6.0'})  
    
            open_this_url = urlopen(req)  
        except (HTTPError, ValueError):
            # print("non valid link")
            flash("invalid link (try using https://)")
            return redirect(url_for('main'))
        
        session['url'] = url
        session['keyword'] = keyword
        
        return redirect(url_for('add'))
    else:
        return render_template('index.html')


@app.route('/add', methods=['POST', 'GET'])
def add():
    if 'url' in session :
        url = session['url']
        keyword = session['keyword']
        try:
            req = Request(url, headers = {'User-Agent': 'Mozilla/6.0'})  
    
            open_this_url = urlopen(req)  
        except (HTTPError, ValueError):
            # print("non valid link")
            flash('invalid link')
            return render_template('index.html')
        
          
            # keyword = request.form.get("keyword")
        keyword = keyword.casefold()
    
        tim = get_load_time(url, open_this_url)
    
        try:
            req = Request(url, headers = {'User-Agent': 'Mozilla/6.0'})  
    
            open_this_url = urlopen(req)  
        except HTTPError as e:
            print(e)
        
        data = BeautifulSoup(open_this_url, "html.parser")
        title = seo_title(keyword, data)
        stop_words = seo_title_stop_words(data)
        title_length = seo_title_length(data)
        key_url = seo_url(url, keyword)
        url_length = seo_url_length(url)
        var_h1 = seo_h1(keyword, data)
        var_h2 = seo_h2(keyword, data)
        var_img = seo_img(keyword, data)
        meta_desc = seo_meta_desc(keyword, data)
        meta_desc_length = seo_meta_desc_length(data)
        robot_txt = get_robots_txt(url)
        
        session.pop("url", None)
        
        
        return render_template('result.html',url = url, tim = tim, title = title,\
        stop_words=stop_words, title_length=title_length, key_url = key_url, \
        url_length = url_length,var_h1 = var_h1, var_h2 = var_h2, var_img = var_img, meta_desc = meta_desc,\
            meta_desc_length = meta_desc_length, robot_txt = robot_txt)
        
    else: 
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.debug = True
    app.run()