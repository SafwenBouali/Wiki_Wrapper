import wikipedia
import unidecode
import json
from bs4 import BeautifulSoup 


def Clean_Text(obj,deleteSpaces=True,deleteNewLines=False):

    res = unidecode.unidecode(obj).replace('-','').replace('=','')
    if deleteNewLines:
        res =res.replace('\n','')
    if deleteSpaces:
        res.replace(' ','').replace("'",'').replace('Inc','').replace(',','').title()
    return res


def Clean_Split(target,split_string='=='):

    temp = '\n\n\n' + split_string + ' '
    res = []
    if (temp in target):
        temp = target.split(temp)
        for tmp in temp:
            t = tmp.split(' '+split_string+'\n')
            if (len(t)==1):
                res.append(Clean_Text(t[0],deleteSpaces=False,deleteNewLines=True))
            elif (len(t)>1):            
                res.append([Clean_Text(t[0],deleteSpaces=False,deleteNewLines=True),Clean_Text(t[1],split_string+'=')])
        return res
    else:
        res.append(Clean_Text(target,deleteSpaces=False,deleteNewLines=True))
        return res


def Try_Get_Main_Image(page):

    soup = BeautifulSoup(page.html(),"html.parser")
    try:
        img = soup.find("a", {"class": "image"})
        return unidecode.unidecode(img.find('img')['src'][2:])
    except:
        return None


def Try_Get_Thumb_Images(page):

    soup = BeautifulSoup(page.html(),"html.parser")
    try:
        images = soup.findAll("div", {"class": "thumbinner"})
        res = []
        for img in images:
            res.append([unidecode.unidecode(img.find('img')['src'][2:]),unidecode.unidecode(img.find('div', {'class','thumbcaption'}).getText())])
        return res
    except:
        return None


def Try_Get_Social_Media_Ref(page):

    res = set()
    for i in page.references:
        if 'facebook' in i.lower() or 'twitter' in i.lower() or 'youtube' in i.lower():
            res.add(unidecode.unidecode(i).replace('http://','').replace('https://',''))
    return list(res)


def Get_Suggestions(input_str):

    suggestions = []
    _list = wikipedia.search(input_str,results=5)
    print _list
    for item in _list:
        success = True
        try:
            name = unidecode.unidecode(item)
            p = wikipedia.page(item)
            summary = unidecode.unidecode(p.summary.split('\n')[0])
            url = Try_Get_Main_Image(p)
        except:
            success = False
        if success:
            suggestions.append([name,url,summary])
    return suggestions


def Get_Page(input_str):
    
    return wikipedia.page(input_str)


def Get_Content(page):

    content = unidecode.unidecode(page.content)
    return Clean_Split(content)


def Get_Title(page):
    
    soup = BeautifulSoup(page.html(),"html.parser")
    text = unidecode.unidecode(soup.find("span",{'class','fn'}).getText())
    return text


def Get_All_Data_On_Page(page):
    
    return {
        'title' : Get_Title(page),
        'summary' : page.summary,
        'main_image' : Try_Get_Main_Image(page),
        'thumb_images' : Try_Get_Thumb_Images,
        'social_media_refs' : Try_Get_Social_Media_Ref(page),
        'content' : Get_Content(page)
    }