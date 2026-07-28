# BTEUP Result Scraper

A Python script that automates fetching student result information from the BTEUP result portal using an enrolment number and date of birth.

The script generates the required request parameters, retrieves the result page, extracts student details and marks, and saves the data for further analysis.

## Features

- Generate request ID from enrolment number and date of birth
- Read multiple student records from a CSV file
- Fetch result pages automatically
- Extract basic student information
- Extract subject-wise marks
- Save detailed logs
- Export marks in a CSV-friendly format

## Project Structure

```
bteup-result-scraper/
│
├── README.md              
├── LICENSE                  
├── requirements.txt          
├── .gitignore               
│
├── main.py                   # Main scraper script
│
├── data.csv              
├── log.txt
└── output.txt     

```

## Requirements

- Python 3.10+
- requests
- beautifulsoup4

Install dependencies

```bash
pip install -r requirements.txt
```

## Input Format

Create a file named `data.csv` in the project directory.

Each line should contain:

```text
Enrolment_Number,Date_of_Birth
```

Example:

```text
E24XXXXXXXXXX01,00/00/0000
E24XXXXXXXXXX02,44/44/4444
```

Do not include a header row.

## Running the Script

```bash
python main.py
```

The script processes each student one by one and creates:

- `output.txt` — student name and obtained marks
- `log.txt` — detailed information for every processed student

## Output Example

```text
E24XXXXXXXXXX01,RXXXXX KXXXXX,45,52,39,60,48
```

## Log

```text
Institute Name : Government Polytechnic Demo
Branch Name    : Information Technology
Student Name   : Student One
ENrollment No. : E24XXXXXXXXXX01

Paper Code : Maximum | Minimum | Obtained

356301 : 60 | 20 | 45
356302 : 60 | 20 | 52
356303 : 60 | 20 | 60
```

## How It Works

1. Read enrolment number and date of birth from the CSV file.
2. Generate the required request parameter.
3. Send a request to the result portal.
4. Parse the returned HTML.
5. Extract student information and marks.
6. Save the extracted data locally.

## Learning Objectives

This project was built to practise:

- HTTP requests
- Web scraping with BeautifulSoup
- HTML parsing
- File handling
- Data extraction
- Working with dictionaries and lists
- Basic automation using Python

## Notes

- The script depends on the current HTML structure of the result portal.
- If the website layout changes, the scraping logic may need to be updated.
- A short delay is added between requests to avoid sending too many requests in a short period.
- This project is intended for educational purposes.

## Future Improvements

- Export directly to CSV or Excel
- Better exception handling
- Progress indicator
- Command-line arguments
- Logging using Python's `logging` module
- Retry mechanism for network failures
- Save complete student data as JSON

## Author

**Aniket Srivastava**

Website: https://srivasani.com

Email: aniket@srivasani.com

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Feedback

If you have any suggestions or find an issue, feel free to open an issue or submit a pull request. I'm always looking to improve my projects and learn from feedback.