import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

#
streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(selection):
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{selection}")
  streamlit.text(fruityvice_response)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('Which fruit would you like to know about')
  if not fruit_choice:
    streamlit.error('Please select fruit to get information')
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
    
except URLError as e:
  streamlit.error()

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

if streamlit.button('Get Fruit Load List'):
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    
# streamlit.stop()

add_my_fruit = streamlit.text_input('Which fruit would you like to add?')

def insert_into_snowflake(add_my_fruit):
  with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('from streamlit')")    
  return "Thanks for adding " + add_my_fruit

if steamlit.button("Add fruit to list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"]) 
  back_from_function = insert_into_snowflake(add_my_fruit)
  streamlit.text(f"Thanks for adding {add_my_fruit}")
