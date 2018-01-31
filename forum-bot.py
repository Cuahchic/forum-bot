# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 20:55:54 2018

@author: colin
"""

from splinter import Browser
import json
from bs4 import BeautifulSoup
import re
import datetime
import time


# Import username and password from JSON file
def load_secrets():
    data = json.load(open('auth/secrets.json'))
    
    return data


# Login to board
def board_login(b, secrets):
    b.visit('https://login.proboards.com/login/5738203/1')
    b.fill('email', secrets['username'])
    b.fill('password', secrets['password'])    
    b.find_by_name('continue').click()


# Get the HTML from the post
def scrape_posts(b, hyperlink, post_type, post_class):
    b.visit(hyperlink)
    
    soup = BeautifulSoup(b.html, 'html.parser')
    
    return soup.findAll(post_type, attrs = {'class': post_class})


# Take the posts list and parse each one for useful information then return what should be inserted into the original post
# TO_DO:
    # Compare post against CSV database of previously found posts and ensure we haven't found it already
    # Write newly found posts to CSV
def create_post_text(posts):
    # What we send back
    text_out = ''
    vowels = ['a', 'e', 'i', 'o', 'u']
    
    # Common regexes
    rPostFaction = re.compile(r'(loreos|garheim|lenfald|outlaws)')
    rMOCs = re.compile(r'[ \t]*(?:outlaws|loreos|lenfald|garheim)[ \t]*\/(?:[A-Za-z \t]*)\/(?:[A-Za-z \t]*)\/(?:[A-Za-z \t]*)')
    rIMG = re.compile(r'<img src="([A-Za-z0-9\/.\_:]+)"')
    
    # Iterate through posts (not first one, as this is where results go)
    for i in range(1, len(posts)):
        post = posts[i]
        
        # Split post into profile and content
        profile = post.find('div', attrs = {'class': 'mini-profile'})
        content = post.find('td', attrs = {'class': 'content'})
        
        # Find username
        
        user = profile.find('a', attrs = {'class': 'user-link'})
        post_user = user.get('title', None)
        
        # Find faction
        post_faction = None
        rPostFactionMatches = rPostFaction.search(profile.text.lower())
        if rPostFactionMatches != None:
            post_faction = rPostFactionMatches[0]
        
        # Find timestamp
        timestamp = content.find('span', attrs = {'class': 'date'}).abbr.get('data-timestamp')
        
        # Get MOC details
        post_text = content.find('div', attrs = {'class': 'message'})
        post_text_lower = str(post_text).lower()
        MOCs = []
        
        for MOC_details in rMOCs.finditer(post_text_lower):
            MOC_details_split = MOC_details.group().split('/')
            
            d = {}
            d['faction'] = MOC_details_split[0].strip()
            d['city'] = MOC_details_split[1].strip()
            d['type'] = MOC_details_split[2].strip()
            d['size'] = MOC_details_split[3].strip()
            
            # Find first image posted after backslash separated description
            if rIMG.search(post_text_lower[MOC_details.end():]) != None:
                d['img'] = rIMG.search(post_text_lower[MOC_details.end():]).groups()[0]
            
            MOCs.append(d)
        
        for MOC in MOCs:
            text_out += 'Player ' + post_user + ((' of faction ' + post_faction.title()) if (post_faction != None) else '') + ' built ' + ('an ' if MOC.get('type')[0] in vowels else 'a ') + MOC.get('type') + ' building in ' + MOC.get('city').title() + '.'
            text_out += ' This was ' + ('an ' if MOC.get('type')[0] in vowels else 'a ') + MOC.get('size') + ' entry for the ' + MOC.get('type') + ' category posted at ' + datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime('%a %d %b %Y %H:%M:%S') + '.'
            text_out += '\n' + ('[img src="{}" style="max-width:100px;"]'.format(MOC.get('img')) if MOC.get('img') != None else '')
            text_out += '\n\n'
        
    return text_out


# Get the new post text and edit it in
# TO_DO:
    # Only edit first post if new entries found
    # Can we parameterise find text etc?
def post_to_thread(b, thread_URL, post_text, sleepTime):
    b.find_by_css('.edit-button').click()
    time.sleep(sleepTime)
    b.find_by_id('menu-item-bbcode').click()
    time.sleep(sleepTime)
    b.find_by_css('.bbcode-editor.editor').find_by_css('textarea').fill(post_text)
    time.sleep(sleepTime)
    b.find_by_name('post').click()    
    time.sleep(sleepTime)
    
    
# Main code
def main():
    try:
        # Load username and password
        secrets = load_secrets()
        
        # URL of thread to monitor
        thread_URL = 'http://merlins-beard.com/thread/1757/chronicling-future-builds'
        
        # Instantiate a browser
        b = Browser()
        
        board_login(b, secrets)
        posts = scrape_posts(b, thread_URL, 'tr', 'post')
        
        new_post_text = create_post_text(posts)
        
        base_post_text = """[i]I'm old, so old.[/i]
    
    [i]Too old to plough the fields. Too old to hammer iron. Too old to fight.[/i]
    
    [i]So now I spend my days at Lion's Head in the company of the other servants of the king, recording his decisions. But I have a secret. In the twilight hours, when I should be asleep, I am keeping a history. There's lots more work to be done, but I want to write down the events of this great land for all future generations. I am in a privileged&nbsp;position to do this as I hear all the comings and goings around the palace.[/i]
    
    ++++++++++++++++++++++
    
    Out of character: this is the thread I am going to use for testing the automation elements. I've got more work to do.
    
    ++++++++++++++++++++++
    
    Posts summary:
    """
        
        post_to_thread(b, thread_URL, base_post_text + new_post_text, 5)
    
    except Exception as e:
        b.quit()
        
    
    b.quit()


main()




