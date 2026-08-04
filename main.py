"""
Created on Tue Jul 28 14:48:09 2026

@author: Aniket Srivastava
website: srivasani.com
email: aniket@srivasani.com
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:43:06 2026

@author: Aniket Srivastava
"""

# For sending htttp requests
import requests

# For regular expression
import re

# For parsing html
from bs4 import BeautifulSoup

# Making a delay in accessing the next student data
# import time

# This is used to generate url_id from enrolment number and date of birth.
# url_id is the string generated uniquely from enrolment number and dob. And when it is added to base url it opens the result page.
# Then id is appended to the default website address.
import base64

# This is for reading csv file.
# Students data must be in comma sepearted value.
# First Value should be Enrolment Number and Second Value should be date of birth.
# Date of birth must be in dd/mm/yyyy format. Remember to add '/' no other character in the date of birth.
import csv

elist = []  # for storing enrolment number
dob = []  # for date of birth dd/mm/yyyy format
sname = []  # student name list
pcode = []  # paper code list
pname = []  # paper name list

# list of list
marks = []  # marks list

# make if false for odd semester
esem = True  # for even semester


# reading data from file storing enrolment and date of birth
def read_data(fname):
    i = 0
    try:
        with open(fname, mode="r") as file:
            csv_reader = csv.reader(file)
            # Loop through each row and extract the enrolment number and date of birth

            for row in csv_reader:
                elist.append(row[0].strip())
                dob.append(row[1].strip())

                print(f"{i+1}. {(elist[i],dob[i])} \n")
                i = i + 1

    except:
        print("Unable to read from file\n")
        return False
    # read is successful
    print("\n######################\n######################\n")

    print(f"Total enrolment numbers: {len(elist)}\n")
    print(f"Total dob: {len(dob)}\n")
    print(f"Total Reads: {i}\n")
    if len(elist) != len(dob):
        print("Wrong Format\n")
        return False
    print("\n######################\n######################\n")
    return True


# burl function takes bool value input and returns string base url


def burl(isevensem):
    base_url = ""
    if isevensem:
        base_url = (
            base_url
            + "https://result.bteexam.com/even/main/CS_RESULT.aspx?id="
        )
    else:
        base_url = (
            base_url
            + "https://test.bteupexam.co.in/Odd_Semester/main/result.aspx?id="
        )

    return base_url


# id generator it generates hash or id from enrolment number and dob
# Make sure enrolment number starts with 'E' not with 'e' and dob has exact same format 'dd/mm/yyyy'
# Because hash will be changed if there is any wrong data


# This function generates the url_id which will be appended to the base_url of the website.
# It takes two values. First is enrolment number and second one is date of birth.
# It returns url_id in string format.
def generate_url_id(id_value: str, dob: str) -> str:
    """
    Predicts the generated code for a given ID and Date of Birth.
    """
    # Convert strings to bytes, encode to base64, then decode back to string
    id_encoded = base64.b64encode(id_value.encode("utf-8")).decode("utf-8")
    dob_encoded = base64.b64encode(dob.encode("utf-8")).decode("utf-8")

    # Format the final string
    final_code = f"{id_encoded}&id2={dob_encoded}"

    return final_code


# takes string as input returns response
def open_website(wurl):
    try:
        response = requests.get(wurl)
        return response

    except:
        print("There is an issue. While connecting to the website...\n")


# takes soup object and appends string and returns true or false
def name_extractor(bsoup):

    tr_tags = bsoup.find_all("tr")  # find all tr_tags list

    # bteup website 'Student Name' ->  align="left", class="printtextbold"
    # align="left", class="printtext" -> actual name
    temp_list = []

    for tr in tr_tags:
        td_tags = tr.find_all("td", align="left")

        for td in td_tags:
            if str(td.text.strip()):
                # print(td.text.strip())
                temp_list.append(td.text.strip())

    if "Student Name" in temp_list:
        i = temp_list.index("Student Name")
        text = temp_list[i + 1]
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        final_text = re.sub(r"\s+", " ", cleaned).strip()
        sname.append(final_text)
        return True

    else:
        return False


#### finds paper code


def paper(bsoup):
    pcodetemp = []  # for paper code
    pnametemp = []  # for paper_name
    tr_tags = bsoup.find_all("tr")  # find all tr_tags list

    for tr in tr_tags:
        td_tags = tr.find_all("td", class_="printtext")
        for td in td_tags:
            text = td.text.strip()
            # check if text is non-empty
            if text:
                try:
                    # paper code is always an integer with 6 digits
                    if text.isdigit() and len(text) == 6:
                        # Avoid duplicates if the same code appears multiple times in a row
                        if int(text) not in pcodetemp:
                            # print(text)
                            pcodetemp.append(int(text))

                            # --- GET THE NEXT TD TEXT which is paper name ---
                            next_td = td.find_next_sibling("td")
                            if next_td:
                                next_text = next_td.text.strip()
                                # print("Next TD Text:", next_text)
                                pnametemp.append(next_text)

                            break  # Stop checking other tds in this row once a valid code is found
                except Exception:
                    pass  # Silently pass instead of printing "error" repeatedly

    # print(pnametemp)
    if len(pcodetemp) == len(pnametemp):
        pcode.append(pcodetemp)
        pname.append(pnametemp)  # add paper names list to plist
        return True
    else:
        return False


# list of all marks or credits student got
# single paper has min three columns --> max_marks, min_marks, obt_marks
# sometimes it may contain other columns --> max_credit, obt_credit


def findmarks(bsoup, idx):

    markstemp = []  # list list [[],[],[],[],[]]

    flist = []  # for storing all marks

    for k in bsoup.find_all(
        "td", style="text-align: center", class_="printtext"
    ):
        mark = k.text.strip()
        # when extracting result of odd semester it also extracts the paper codes with it
        # paper code have six digits
        # exclude paper code to be in the list it is necessary to check mark length is below 6
        if len(str(mark)) < 6:
            flist.append(mark)

    step = int(len(flist) / len(pcode[idx]))  # number of columns for a paper

    for i in range(
        0, len(flist), step
    ):  # get list of fixed length that is columns per paper code
        # store in a temporary list
        markstemp.append(flist[i : (i + step)])

    if markstemp:
        marks.append(markstemp)
        return True
    else:
        return False


print("\n######################\n######################\n")
print(
    "Please make sure 'data.csv' has enrolment(E24XXXXXXXXXXXX), dob (dd/mm/yyyy format)"
)
print("\n######################\n######################\n")

# Ask for even or odd semester
semester = input("Please Enter 1 for odd semester: ")

try:
    if int(semester) == 1:
        esem = False
        print("Setting base url to odd semester... \n")
    else:
        print("Base url is set to even semester... \n")
except:
    pass

# ask for file name
fname = input("Please enter file name(with extension): ")

try:
    isfrs = read_data(fname)  # store true or false
    if isfrs:
        print("File successfully parsed and loaded.\n")
    else:
        print("Unable to load the file. \n")
except:
    print(
        "Make sure file exists in the same folder and name provided with extension like 'data.csv'"
    )


# connect to the website


i = 0
while i < len(elist):
    # elist = [e1,e2,e3, dob4]
    # dob = [dob1, dob2, dob3, dob4]

    # generate uid
    uid = generate_url_id(elist[i], dob[i])
    url = burl(esem) + uid

    print("\n*************************\n*************************\n")
    print(f"\n{i+1}. Generating url id for {elist[i]} ...\n")
    print(f"{url}\n")

    # connect to the website

    response = open_website(url)

    if response.status_code == 200:
        print("Getting response...\n")

        # get response text
        text = response.text

        soup = BeautifulSoup(text, features="html.parser")

        # extract the name
        nes = name_extractor(soup)
        print("Extracting Name...\n")
        if nes:
            print(f"Name: {sname[i]} extracted succesfully...\n")

            print(
                "\n-------------------------------------------------------------\n"
            )
        else:
            print("Unable to extract the name...")

        # extract all the paper codes and paper names
        # pcode [[p1,p2,p3,4,p5,...], [...],  [...]      ]
        pes = paper(soup)

        print("Extracting Paper Codes and Paper Names...\n")
        if pes:  # paper extracted successfully
            print(f"Paper Code: {pcode[i]} extracted succesfully...\n")
            print(f"Paper Name: {pname[i]} extracted succesfully...\n")
            print(f"Total Papers: {len(pcode[i])} Extracted...\n")
            print(
                "\n-------------------------------------------------------------\n"
            )

        else:
            print("Unable to extract paper code and paper name...\n")

        # extract all the marks
        # marks --> [ [ [m1,m2,m3,m4,m5], [m1, m2, m3, m4, m5], [...]             ], [...], [...],...             ]
        mes = findmarks(soup, i)
        print("Extracting Marks...\n")
        if mes:  # marks extracted succesfully
            print(f"Marks: {marks[i]} extracted succesfully...\n")
            print(f"Total Marks: {len(marks[i])} Extracted...\n")
            print(
                "\n-------------------------------------------------------------\n"
            )
        else:
            print("Unable to extract paper code and paper name...\n")

        # write on console and log file
        print("\n*************************\n*************************\n")
        print("Writing in 'log.txt' and 'output.txt' file... \n")

        etemp = (
            str(i + 1)
            + ". Enrolment Number: "
            + str(elist[i])
            + "\n"
            + "Name: "
            + str(sname[i])
            + "\n"
        )

        with open("log.txt", "a") as file:
            file.write(
                "\n*************************\n*************************\n"
            )
            file.write(etemp)

        # write in output file
        with open("output.txt", "a") as f:
            f.write(f"\n{elist[i]}, {sname[i]}")

        print(etemp)

        pn = 0  # for interating in paper name list
        for pc in pcode[i]:
            # write in log file
            with open("log.txt", "a") as file:
                file.write(
                    f"\t{pn+1}. ({pc}, {pname[i][pn]}): {marks[i][pn]}\n"
                )

            # write in output.txt
            # enrolment, name, ob_marks1, ob_marks2
            # obtained marks are always at position 2

            with open("output.txt", "a") as f:
                # check for length must not less than three
                if len(marks[i][pn]) >= 3:
                    f.write(f", {marks[i][pn][2]}")
                else:
                    print(
                        "\nUnable to extract obtained marks from the marks list..."
                    )

            print(f"\t{pn+1}. ({pc}, {pname[i][pn]}): {marks[i][pn]}\n")
            pn = pn + 1

        with open("log.txt", "a") as file:
            file.write(
                "\n*************************\n*************************\n"
            )

        print("\nRecord written in file succesfully... \n")
        print("\n*************************\n*************************\n")

    else:
        print(f"{response.status_code}: Unable to connect to the website...\n")

    i = i + 1













