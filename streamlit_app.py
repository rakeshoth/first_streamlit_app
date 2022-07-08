
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Har-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toasts')


# Display the table on the page.
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)  
  fruityvice_normalized = ps.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    #fruitvice_requests = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)  
    #streamlit.text(fruitvice_requests.json())
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()
    
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("Hello from Snowflake:")
streamlit.text("The fruit load list contains:")
streamlit.dataframe(my_data_row)


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.text('Thanks for adding '+add_my_fruit)
