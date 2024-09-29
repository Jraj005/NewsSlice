import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import requests
from io import BytesIO

# Download necessary NLTK resources
nltk.download('punkt')

st.set_page_config(page_title='NewsSlice: A Summarised News Portal', page_icon='📰')


def fetch_news_search_topic(topic):
    try:
        site = 'https://news.google.com/rss/search?q={}'.format(topic)
        op = urlopen(site)  # Open that site
        rd = op.read()  # Read data from site
        op.close()  # Close the object
        sp_page = soup(rd, 'xml')  # Scraping data from site
        news_list = sp_page.find_all('item')  # Finding news
        return news_list
    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return []


def fetch_top_news():
    try:
        site = 'https://news.google.com/news/rss'
        op = urlopen(site)  # Open that site
        rd = op.read()  # Read data from site
        op.close()  # Close the object
        sp_page = soup(rd, 'xml')  # Scraping data from site
        news_list = sp_page.find_all('item')  # Finding news
        return news_list
    except Exception as e:
        st.error(f"Error fetching top news: {e}")
        return []


def fetch_category_news(topic):
    try:
        site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
        op = urlopen(site)  # Open that site
        rd = op.read()  # Read data from site
        op.close()  # Close the object
        sp_page = soup(rd, 'xml')  # Scraping data from site
        news_list = sp_page.find_all('item')  # Finding news
        return news_list
    except Exception as e:
        st.error(f"Error fetching category news: {e}")
        return []


def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except Exception:
        image = Image.open('./Meta/no_image.jpg')
        st.image(image, use_column_width=True)


def display_news(list_of_news, news_quantity):
    c = 0
    for news in list_of_news:
        c += 1
        st.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(f"Error processing article: {e}")
            continue  # Skip to the next article if there’s an error

        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)
        if c >= news_quantity:
            break


def run():
    st.title("NewsSlice: News Made Simple")
    shared_link = "https://drive.google.com/file/d/1K1fzEgjXHO2gOMUAPvJ6HEvHyvKaLFFC/view?usp=sharing"
    # Extract the file ID from the link
    file_id = shared_link.split('/d/')[1].split('/')[0]
    # Construct the download URL
    download_url = f"https://drive.google.com/uc?id={file_id}"

    # Fetch the image
    response = requests.get(download_url)
    response.raise_for_status()  # Check for request errors

    # Open the image
    image = Image.open(BytesIO(response.content))
    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("")

    with col2:
        st.image(image, use_column_width=False)

    with col3:
        st.write("")
    
    category = ['Trending🔥 News', 'Favourite💙 Topics', 'Search🔍 Topic']
    cat_op = st.selectbox('Select your Category', category)
    
    # if cat_op == category[0]:
    #     st.warning('Please select Type!!')
    if cat_op == category[0]:
        st.subheader("✅ Here is the Trending🔥 news for you")
        no_of_news = 15
        news_list = fetch_top_news()
        display_news(news_list, no_of_news)
    elif cat_op == category[1]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = 15
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader("✅ Here are some {} News for you".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(chosen_topic))

    elif cat_op == category[2]:
        user_topic = st.text_input("Enter your Topic🔍")
        no_of_news = 15

        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here are some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Topic Name to Search🔍")


run()
