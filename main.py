from urllib.request import urlopen, Request
import time
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import io

def get_load_time(url, open_this_url):

    # if ("https" or "http") in url:  
    #     open_this_url = urlopen(url)  
    # else:
    #     open_this_url = urlopen("https://" + url)  
    # try:
    #     req = Request(url, headers = {'User-Agent': 'Mozilla/6.0'})  
    #     open_this_url = urlopen(req) 
    # except HTTPError as e:
    #     print(e)
        
        
    start_time = time.time()  
    open_this_url.read()  
    end_time = time.time()  
    open_this_url.close()  
    time_to_load = end_time - start_time
    
    if time_to_load < 2:
        result = f"\nThe time taken to load {url} is {time_to_load:.2} seconds. Your time is optimal"
    else: 
        result = f"\nThe time taken to load {url} is {time_to_load:.2} seconds. Your time is NOT optimal"

    return result



def seo_title(keyword, data):
    if data.title:
        if keyword in data.title.text.casefold():
            status = "Found"
        else:
            status = "Not found"
    else:
        status = "No title found"
    return status

def seo_title_stop_words(data):
    words = 0
    list_words = []
    if data.title:
        with open('stopwords.txt', 'r') as f:
            for line in f:
                if re.search(r'\b' + line.rstrip('\n') + r'\b', data.title.text.casefold()): #look for a regular expression
                    words += 1
                    list_words.append(line.rstrip('\n'))
        if words > 0:
            stop_words = "We found {} stop words in your title. they sould be removed : {} ".format(words, list_words)
        else: 
            stop_words = "We found no stop words"
    else:
        stop_words = "We could not find a title"
    return stop_words 


def seo_title_length(data):
    if data.title:
        if len(data.title.text) < 60:
            length = "Your length is under the maximum suggested of 60 characters. Your title respects the guidelines of seo: {} characters.".format(len(data.title.text))
        else: 
            length = "Your length is over the max suggested of 60 characters. Try to minimize the words count. Your title is {} characters".format(len(data.title.text))
    else: 
        length = "No title was found"
        
    return length

def seo_url(url, keyword):
    if url: 
        if keyword in url.casefold():
            slug = "Your keyword was found in your slug"
        else:
            slug = "Your keyword was not found in your slug"
    else:
        slug = "No url was returned"
    return slug


def seo_url_length(url):
    if url:
        if len(url) < 100:
            url_length = "Your URL is less than the 100 character maximum suggested. it's {} characters.".format(len(url))
        else: 
            url_length = "Your URL is over 100 characters. You should change it. It's {} characters.".format(len(url))
    else:
        url_length = "Your URL was not found"
    return url_length

def seo_h1(keyword, data):
    if data.h1:
        tags = data.find_all('h1')
        if len(tags) > 1:
            h1_tag = "You have more than one h1 tag. You MUST have just one."
        else:
            tag = str(tags[0]).casefold()
            if keyword in tag:
                h1_tag = "Keyword was found in your h1 tag. And you have one h1 tag. Perfect work yeeeeey !!!"
            else: 
                h1_tag = "You have one h1 tag. But Keyword was not found in you h1 tag."
            
    else: 
        h1_tag = "No h1 Tags Found. You should create one and just one."
    return h1_tag


def seo_h2(keyword, data):
    if data.h2:
        all_tags = data.find_all('h2')
        for tag in all_tags:
            tag = str(tag.string)
            if keyword in tag.casefold():
                h2_tag = "found your keyword in at least one h2 tag. And that's great !!!"
                break
            else: 
                h2_tag = "We did not find your keyword in a single h2 tag. You should add \"{}\" to h2 tag".format(keyword)
    else: 
        h2_tag = "We couldn't find any h2 tags. You should add a few. "
    return h2_tag

def seo_img(keyword, data):
    x = []
    if data.img:
        
        for imag in data.find_all('img'):
            result = ""
            if imag.get('alt') != None:
                # print(imag.get('alt'))
                # result = ""
                if keyword in imag.get('alt').casefold():
                    x.append("the image with the source : {} does have an \"alt\" tag and does have kayword.".format(imag.get('src')))
                else: 
                    x.append(" the image with the source : {} does have an \"alt\" tag but it needs a proper implementation of the keyword.".format(imag.get('src')))
            else:
                x.append("You should add an alt tag to the image with the source: {}".format(imag.get('src')))
    else:
        x.append("There's no images in your webside. You should add some to make it more welcoming.")
    return x

def seo_meta_desc(keyword, data):
    result = ""
    count = 0
    if data.meta:
        for meta in data.find_all('meta'):
            if meta.get('name') == 'description':
                # print(meta.get('content'))
                count += 1
                if keyword in meta.get('content'):
                    result = "Your meta description does contain the keyword. Good Job !  \n"
                else:
                    result = "You should add the keywords to your description for better optimization \n"
        if count == 0:
            result = "there is no meta description tag in your website"
                
    else:
        result = "there no meta tags in your website. You should add some for better indexation"
                    
    return result

def seo_meta_desc_length(data):
    leng = ""
    count = 0
    if data.meta:
        for meta in data.find_all('meta'):
            if meta.get('name') == 'description':
                count += 1
                if len(meta.get('content')) > 256:
                    leng = "You optimize you description length {}".format(len(meta.get('content')))
                else: 
                    leng = "The length of your description is optimal : {}".format(len(meta.get('content'))) 
        if count == 0:
            leng = "there is no meta description tag in your website" 
        
    else:
        leng = "there no meta tags in your website. You should add some for better indexation"
    return leng

def get_robots_txt(url):
    if url.endswith('/'):
        path = url
    else: 
        path = url + '/'
        
    try:
        list = []
        dic = {}
        list2 = []
        list3 = []
        req = Request(path + "robots.txt", headers = {'User-Agent': 'Mozilla/6.0'})  
        # # if ("https" or "http") in url:  # Checking for presence of protocols
        open_url = urlopen(req)  # Open the url as entered by the user
        
        
        text_file = open("robot.txt", "w")
        
        robot_txt_data = io.TextIOWrapper(open_url, encoding='utf-8')
        result = "here is your robots.txt, check if these are the pages you want the web crawler not to access to : \n "
        text_file.write(robot_txt_data.read())
        text_file.close()
        text_file = open("robot.txt", "r")
        for line in text_file:
            if line != "\n":
                list.append(line.split("\n"))
        for item in list:
            list2.append(item[0])
            
        for elm in list2:
            if "Disallow" in elm:
                value = elm.split(":")[1]
                list3.append(value)
        
        
        
        return list3
    except HTTPError as e:
        print(e)
    
        result = "this url does not have a robot.txt file"
        return result
