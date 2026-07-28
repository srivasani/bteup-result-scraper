"""
Created on Tue Jul 28 14:48:09 2026

@author: Aniket Srivastava
website: srivasani.com
email: aniket@srivasani.com
"""

# For sending htttp requests
import requests

# For parsing html
from bs4 import BeautifulSoup

# Making a delay in accessing the next student data
import time

# This is used to generate url_id from enrolment number and date of birth.
# url_id is the string generated uniquely from enrolment number and dob. And when it is added to base url it opens the result page.
# Then id is appended to the default website address.
import base64

# This is for reading csv file.
# Students data must be in comma sepearted value.
# First Value should be Enrolment Number and Second Value should be date of birth.
# Date of birth must be in dd/mm/yyyy format. Remember to add '/' no other character in the date of birth.
import csv


# This function generates the url_id which will be appended to the base_url of the website.
# It takes two values. First is enrolment number and second one is date of birth.
# It returns url_id in string format.
def generate_url_id(id_value: str, dob: str) -> str:
    """
    Predicts the generated code for a given ID and Date of Birth.
    """
    # Convert strings to bytes, encode to base64, then decode back to string
    id_encoded = base64.b64encode(id_value.encode('utf-8')).decode('utf-8')
    dob_encoded = base64.b64encode(dob.encode('utf-8')).decode('utf-8')
    
    # Format the final string
    final_code = f"{id_encoded}&id2={dob_encoded}"
    
    return final_code
    


# Open the CSV file in read mode
# file name is data.csv must be in the same directory where this file is located. Make sure it has '.csv' format.
# Format of file is enrolment number, date of birth in dd/mm/yyyy 
# Strcture of file is given below. Without any blank line. There should be no header.

'''
E24XXXXXXXXXX20, 00/00/2000
E24XXXXXXXXXX21, 01/01/2001
'''

with open('data.csv', mode='r') as file:
    # Create a reader object
    csv_reader = csv.reader(file)
    
    # Loop through each row and extract the enrolment number and date of birth
    for row in csv_reader:
        
        # Mistake: Do not remove strip() function
        # row[0] ==> enrolment number
        # row[-1] ==> date of birth
        
        # calling gnerate_url_id function and stores the unique url_id in result variable
        result = generate_url_id(row[0].strip(), row[-1].strip())
     
        base_url = "https://test.bteupexam.co.in/Odd_Semester/main/result.aspx?id="
        url = base_url + result
            

            
        # Sending request and stroing the response received from the result page
        # This object stores raw html from result page if successful connection
        
        try:
            response = requests.get(url)
            
            if (response.status_code==200):
                print("Getting Response...\n")
            
        except:
            print("There is an issue. While connecting to the website...\n")
            break # get out of the loop

            
        text = response.text
            
        soup = BeautifulSoup(text, features="html.parser")
            

           
        trS = soup.find_all("tr") # Get the list of tr tags 

            
        # This stores "Institute Name","Branch Name", "Student Name", "Roll Number", and "ENrollment No".
        # Note these are name of keys. 
        basic_info = {} 
        
        # In this range values of basic_info exits such as "Institute Name","Branch Name", "Student Name", "Roll Number", and "ENrollment No".
        for i in range(5,9):
            
            # On the result page basic_info headings have "printtextbold" class common 
            # And values have "printtext" class common. Based on this we are finding all values.
            
            # List of keys of basic_info
            keys = trS[i].find_all("td", class_="printtextbold")
            
            # List of Values of basic_info
            vals = trS[i].find_all("td", class_="printtext")
            
            # Adding every single (key, value) pair in dictionary
            j = 0
            while(j<len(keys)):
                key = keys[j].text.strip()
                val = vals[j].text.strip()
                    
                basic_info[key] = val
                j = j+1
            
        # This stores paper_code as key and a list containing [max_marks, min_marks, obtained_marks] in the subject 
        '''
        {paper_code:[max_marks, min_marks, obtained_marks],...}
        
        {356301:[60,20,29], 356302: [60, 20, 49], ...}
        
        '''
        marks = {}
            
            
        # All marks_data paper_code, max_marks, min_marks, obtained marks have common class  "printtext" and common style "text-alight:center"
        # As Subject name does not share these common attribute we cannot parse it from the data received from the website
        '''
        marks_data = [paper_code1, max_marks_in_paper1, min_marks_in_paper1, obtained_marks_in_paper1, 
                      paper_code2, max_marks_in_paper2, min_marks_in_paper2, obtained_marks_in_paper2, 
                      ....
                      ....
                      ]
        '''
        marks_data = trS[9].find_all("td", class_="printtext", style="text-align: center")
        
        # This adds all paper_code and marks in the marks dictionary
        j = 0
        while j<len(marks_data):
            paper_code = marks_data[j].text.strip()
            max_marks = marks_data[j+1].text.strip()
            min_marks = marks_data[j+2].text.strip()
            obtained_marks = marks_data[j+3].text.strip()
                
            marks[paper_code] = [max_marks,min_marks,obtained_marks]
             
            # Each fourth entry in marks_data list is new paper
            # Zeroth index in the marks_data list is paper_code
            # As there are three type of marks max_marks, min_marks, obtained_marks
            j = j+4
        
        # Create log file 
        # log file contains all details for reference which are printed on the console
        with open("log.txt","a") as file:
                file.write("\n************************\n") 
                
                
        # Prints Basic Information of Student on the console    
        print("\n############################\n")
        for i in basic_info:
            
            # Write the details which are printed on the console in log file
            with open("log.txt","a") as file:
                file.write(f"{i}: {basic_info[i]}\n")
            
            # key: value from basic_info dictionary is printed in console
            print(i, ": ", basic_info[i])

         # Write the details which are printed on the console in log file in the same format
        with open("log.txt","a") as file:
            file.write("\n--------------------------\n")
            file.write("Paper Code : Maximum Marks | Minimum Marks | Obtained Marks")
            file.write("\n--------------------------\n")
               
        print("\n--------------------------\n")
            
        print("Paper Code : Maximum Marks | Minimum Marks | Obtained Marks")
            
        print("\n--------------------------\n")
            
        # Prints Marks of Student on the Console   
        for j in marks:
            
            # Write the printed console data in log file
            with open("log.txt","a") as file:
                file.write(f"{j}: {marks[j][0]}, {marks[j][1]} {marks[j][2]}\n")
                
                # j is key from marks list it represents paper code
                # There is a value associated with this key.
                # Value is list of three type of marks in the paper.
                # max_marks, min_marks, obtained_marks in the paper
            print(j, ": ", marks[j][0], marks[j][1], marks[j][2])

        with open("log.txt","a") as file:
                file.write("\n************************\n")
                
        print("\n############################\n")
        
        

        # output file stores enrolment number, and marks of all subject without paper code
        # Format of output file is csv but saved as txt file
        # You can import it in excel very easily
        # Open file in append mode 
        with open("output.txt", "a", encoding="utf-8") as file:
            # This line makes enrolment number and Name 
            # E24XXXXXXXXXX20, RXXXX KXXXX in string format
            output_data = basic_info['ENrollment No.'] + "," + basic_info['Student Name'] 

            # obtained_marks of each subject are added in the output_data string
            for m in marks:
                output_data = output_data +"," + marks[m][-1]
            
            # output_data string is written on the file
            # This file does contain any paper code
            # All obtaned marks in the serial wise on the resutl page
            # For more information about the papers of individual student log file or console can be referred.
            '''
            enrolment_number,name,obtained_marks_sub1, obtained_marks_sub2,...
            E24XXXXXXXXXX20,RXXXX KXXXX,30,40,50,60,...
            '''
            file.write(f"{output_data}\n")
            
            
        # Wait before accessing details of another student
        time.sleep(1)














