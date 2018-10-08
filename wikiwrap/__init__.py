name = "wikiwrap"

import wikipedia
import unidecode
import json
from bs4 import BeautifulSoup




class page:
    """a class that has all the wrapped operations of a page"""

    def get_suggestions(input_str,max_res=3):

        suggestions = []
        _list = wikipedia.search(input_str,results=max_res)
        for item in _list:
            _recap = page(item,init_mode='suggest')
            suggestions.append([_recap.title,_recap.url,_recap.summary,_recap.main_image])
        return suggestions



    def __clean_text(obj,deleteSpaces=True,deleteNewLines=False):

        res = unidecode.unidecode(obj).replace('-','').replace('=','')
        if deleteNewLines:
            res =res.replace('\n','')
        if (deleteSpaces):
            res.replace(' ','').replace("'",'').replace('Inc','').replace(',','').title()
        return res


    def __clean_split(target,split_string='=='):

        temp = '\n\n\n' + split_string + ' '
        res = []
        if (temp in target):
            temp = target.split(temp)
            for tmp in temp:
                t = tmp.split(' '+split_string+'\n')
                if (len(t)==1):
                    res.append(__clean_text(t[0],deleteSpaces=False,deleteNewLines=True))
                elif (len(t)>1):
                    res.append([__clean_text(t[0],deleteSpaces=False,deleteNewLines=True),Clean_Text(t[1],split_string+'=')])
            return res
        else:
            res.append(__clean_text(target,deleteSpaces=False,deleteNewLines=True))
            return res

    def __get_summary(_page):
 
        return unidecode.unidecode(_page.summary.split('\n',1)[0])


    def __init__(self,name,init_mode='full'):

        self.page = wikipedia.page(name)
        self.__soup = BeautifulSoup(self.page.html(),"html.parser")
        self.title = unidecode.unidecode(self.page.title)
        self.main_image = []
        try:
            temp = unidecode.unidecode(self.__soup.find("a", {"class": "image"}).find('img')['src'][2:])
            self.main_image.append(temp)
            self.main_image.append(temp.replace('/thumb','').rsplit("""/""", 1)[0])
        except:
            print("no main image found.")
        if (init_mode is 'suggest'):
            self.url = unidecode.unidecode(self.page.url)
            self.summary = page.__get_summary(self.page)
        elif (init_mode is 'full'):
            self.thumb_images = []
            try:
                images = self.__soup.findAll("div", {"class": "thumbinner"})
                for img in images:
                    self.thumb_images.append([unidecode.unidecode(img.find('img')['src'][2:]),unidecode.unidecode(img.find('div', {'class','thumbcaption'}).getText())])
            except:
                print("no thumb images found.")
            self.social_media_refs = []
            try:
                for i in self.page.references:
                    temp = i.lower()
                    if (
                        'facebook' in temp
                        or 'twitter' in temp
                        or 'youtube' in temp
                        ):
                        self.social_media_refs.append(unidecode.unidecode(i).replace('http://','').replace('https://',''))
            except:
                print("no social media references found.")
            self.content = unidecode.unidecode(__clean_split(self.page.content))