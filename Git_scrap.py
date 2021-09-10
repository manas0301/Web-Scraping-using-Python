import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
url='https://github.com/topics'
r = requests.get(url)
content = r.content
# print(content)
doc = BeautifulSoup(content, 'html.parser')
# print(soup.prettify)
selection_class = "f3 lh-condensed mb-0 mt-1 Link--primary"
topic_title_tags = doc.find_all('p', {'class': selection_class})
# print(len(topic_title_tags))
# print(topic_title_tags)

desc_selector = "f5 color-text-secondary mb-0 mt-1"
topic_desc_tags = doc.find_all('p', {'class': desc_selector})
# print(topic_desc_tags)

topic_title_tag0=topic_title_tags[0]
div_tags=topic_title_tag0.parent
topic_link_tags = doc.find_all('a', {'class': 'd-flex no-underline'})
# print(len(topic_title_tags))

# print(topic_link_tags[0]['href'])
topic0_url = "https://github.com" + topic_link_tags[0]['href']
# print(topic0_url)

topic_titles = []
topic_descs = []

for tag in topic_title_tags:
    topic_titles.append(tag.text)
# print(topic_titles)

for tag in topic_desc_tags:
    topic_descs.append(tag.text.strip())  #strip.append_will_remove extra spaces from the start an end.
# print(topic_descs)

topic_urls = []
base_url = "https://github.com"

for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])
# print(topic_urls)


#Creating csv files


topics_dict = {'title': topic_titles, 'description': topic_descs, 'url': topic_urls}  #creating a dictionary to store title, description & urls.
topics_df = pd.DataFrame(topics_dict)    #using lists in dictionary to create a dataframe 
# print(topics_df)

topics_df.to_csv('topics.csv' , index = None)

#Getting information out of the topic page

topic_page_url = "https://github.com/topics/3d"
response = requests.get(topic_page_url)
html_content = response.content
# print(html_content)
topic_doc = BeautifulSoup(html_content, 'html.parser')
# print(topic_doc)

h1_selection_class = "f3 color-text-secondary text-normal lh-condensed"
repo_tags = topic_doc.find_all('h1', {'class': h1_selection_class})  #fetching the repositories of the topics
# print(repo_tags)

a_tags = repo_tags[0].find_all('a')        
# print(a_tags[0].text.strip())
# print(a_tags[1].text.strip())
# print(a_tags[1]['href'])
repo_url = base_url + a_tags[1]['href']
# print(repo_url)

star_tags = topic_doc.find_all('a', { 'class': "social-count float-none"})
# print(len(star_tags))
# # print(star_tags[0].text.strip())

def get_repo_info(h1_tag, star_tag):
    # returns all the required info about a repository
    a_tags = h1_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url =  base_url + a_tags[1]['href']
    stars = star_tag.text.strip()
    return username, repo_name, stars, repo_url


# get_repo_info1 = get_repo_info(repo_tags[0], star_tags[0])
# print(get_repo_info1)
topic_repos_dict = {'username': [], 'repo_name' : [], 'stars': [], 'repo_url': []}


for i in range(len(repo_tags)):
    repo_info = get_repo_info(repo_tags[i], star_tags[i])
    topic_repos_dict['username'].append(repo_info[0])
    topic_repos_dict['repo_name'].append(repo_info[1])
    topic_repos_dict['stars'].append(repo_info[2])
    topic_repos_dict['repo_url'].append(repo_info[3])

# print(topic_repos_dict)

topic_repos_df = pd.DataFrame(topic_repos_dict)
# print(topic_repos_df)


def get_topic_page(topic_url):
    # Download the page
    response = requests.get(topic_url)
    # Check successful response
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    # Parse using Beautiful soup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def get_repo_info(h1_tag, star_tag):
    # returns all the required info about a repository
    a_tags = h1_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url =  base_url + a_tags[1]['href']
    stars = star_tag.text.strip()
    return username, repo_name, stars, repo_url


def get_topic_repos(topic_doc):
    # Get the h1 tags containing repo title, repo URL and username
    h1_selection_class = 'f3 color-text-secondary text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h1', {'class': h1_selection_class} )
    # Get star tags
    star_tags = topic_doc.find_all('a', { 'class': 'social-count float-none'})
    
    topic_repos_dict = { 'username': [], 'repo_name': [], 'stars': [],'repo_url': []}

    # Get repo info
    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], star_tags[i])
        topic_repos_dict['username'].append(repo_info[0])
        topic_repos_dict['repo_name'].append(repo_info[1])
        topic_repos_dict['stars'].append(repo_info[2])
        topic_repos_dict['repo_url'].append(repo_info[3])
        
    return pd.DataFrame(topic_repos_dict)

# get_topic_repos(get_topic_page(topic_urls[6])).to_csv('ansible.csv', index= None)

def scrape_topic(topic_url, topic_name):
    fname = topic_name + '.csv'
    if os.path.exists(fname):
        print("File {} already exists. Skipping this file..".format(fname))
        return
    topic_df = get_topic_repos(get_topic_page(topic_url))
    topic_df.to_csv(fname, index=None)


# url4 = topic_urls[4]
# topic4_doc = get_topic_page(url4)
# topic4_repos = get_topic_repos(topic4_doc)
# topic_repos_df = pd.DataFrame(topic_repos_dict)

# Now we  write a single function to:
# 1) get the list of topics page.
# 2) get the list of top repositories from the individual topic pages
# 3) for each topic,  we create a seperate CSV file of the top repositories.

def get_topic_titles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': selection_class})
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

def get_topic_descs(doc):
    desc_selector = 'f5 color-text-secondary mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': desc_selector})
    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    return topic_descs

def get_topic_urls(doc):
    topic_link_tags = doc.find_all('a', {'class': 'd-flex no-underline'})
    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
    return topic_urls

def scrape_topics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    doc = BeautifulSoup(response.text, 'html.parser')
    topics_dict = {
        'title': get_topic_titles(doc),
        'description': get_topic_descs(doc),
        'url': get_topic_urls(doc)
    }
    return pd.DataFrame(topics_dict)


# print(scrape_topics())

def scrape_topics_repos():
    print('Scraping list of topics')
    topics_df = scrape_topics()
    
    # os.makedirs('data', exist_ok=True)
    for index, row in topics_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['title']))
        scrape_topic(row['url'], row['title'])

scrape_topics_repos()
