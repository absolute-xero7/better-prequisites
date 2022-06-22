"""Scrapes the prerequisites of a course from the University of Toronto's course website and then
take the user-inputted course and tell us the courses which need the user-input course as a
prerequisite. """
from pprint import pprint

import requests
from bs4 import BeautifulSoup

target_course = input("Enter the course you wanna look up: ")
target_course = target_course.upper()
target_course = target_course.replace(" ", "")
target_course = target_course.replace("-", "")
target_course = target_course[0:6]

target_course_use = []

course_cards = []
course_cards_dict = {}
# Only using BR 5
course_page_html_dict = {}  # Stores the html content of each BR 5 course page.
for i in range(17):
    course_html = BeautifulSoup((requests.get(
        'https://artsci.calendar.utoronto.ca/search-courses?course_keyword=&field_section_value'
        '=All&field_prerequisite_value=&field_breadth_requirements_value=The%20Physical%20and'
        '%20Mathematical%20Universes%20%285%29&field_distribution_requirements_value=All&page=' +
        str(i)).content), "html.parser").find("div", {"class": "view-content"})
    course_page_html_dict['course_page' + str(i)] = course_html

# print(course_page_html_dict['course_page0'].find_all('div', class_='views-row')[10].h3.text)

# test_course_list = course_page_html_dict['course_page0'].find_all('div', class_='views-row')
# print(test_course_list[0].find(class_='views-field views-field-field-prerequisite').text)

for i in range(17):
    course_cards.extend(
        course_page_html_dict['course_page' + str(i)].find_all('div', class_='views-row'))

del course_cards[1::2]

for course_big in course_cards:
    course_name = str(course_big.h3.text)
    course_name = course_name.replace(" ", "")
    course_name = course_name[0:6]
    try:
        course_prerequisite_raw = str(
            course_big.find(class_='views-field views-field-field-prerequisite').text)
    except AttributeError:
        continue
    course_prerequisite_raw = course_prerequisite_raw.replace('Prerequisite:', '')
    course_prerequisite_raw = course_prerequisite_raw.replace(" ", "")
    course_prerequisite_raw = course_prerequisite_raw.replace("/", ",")
    course_prerequisite_raw = course_prerequisite_raw.replace("(", "")
    course_prerequisite_raw = course_prerequisite_raw.replace(")", "")
    course_prerequisite_raw = course_prerequisite_raw.replace("[", "")
    course_prerequisite_raw = course_prerequisite_raw.replace("]", "")
    course_prerequisite_raw = course_prerequisite_raw.split(',')
    course_prerequisite = []
    for course in course_prerequisite_raw:
        course_prerequisite.append(course[0:6])
    course_cards_dict[
        course_name] = course_prerequisite  # Now I have a dictionary of all the courses and their prerequisites (list of strings)

for course in course_cards_dict:
    if target_course in course_cards_dict[course]:
        target_course_use.append(course)

print(target_course_use)







