# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 20:55:54 2018

@author: colin
"""

from splinter import Browser
import json
from bs4 import BeautifulSoup


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
def create_post_text(posts):
    results = 
    # Get all posts that aren't the first one
    # Compare post against CSV database of previously found posts and ensure we haven't found it already
    # For each post read the message and do a regex for (.*)\/(.*)\/(.*)\/(.*) to find any instances of entries
    # Read previously formatted entries from first post and add new entries into this using BBCode formatting
    # Write newly found posts to CSV
    # Return newly formatted entries
    
    
# Main code
def main():
    secrets = load_secrets()
    
    b = Browser()
    
    board_login(b, secrets)
    posts = scrape_posts(b, 'http://merlins-beard.com/thread/1757/chronicling-future-builds', 'tr', 'post')

    new_post_text = create_post_text(posts)
    
    # Find button to edit first post
    # Switch to BBCode view
    # Replace or append this with new_post_text
    # Submit


main()




