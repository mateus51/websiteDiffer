from bs4 import BeautifulSoup as beautiful_soup
from pathlib import Path
import downloader


url = "http://homepages.dcc.ufmg.br/~figueiredo/disciplinas/2016b/dcc603/"
original_json = Path("./original_data.json")


# If the user doesn't have any data to compare, download the original version
if not original_json.is_file():
	print("You don't have the original data! We're going to download it right now!")
	content = downloader.download_webpage(url)
	soup = beautiful_soup(content, "html.parser")
	table = soup.find("table")

	file_dict = downloader.extract_table_data(table)

	downloader.save_dict_to_json(file_dict, "original_data.json")

# Now that is guaranteed that we have the original data, download a newer version

print("We're downloading a newer version...")	

content = downloader.download_webpage(url)
soup = beautiful_soup(content, "html.parser")
table = soup.find("table")

file_dict = downloader.extract_table_data(table)

# Save the data to the new_data.json file
downloader.save_dict_to_json(file_dict, "new_data.json")

# Check to see any differences between the two JSON files.
# If there's any difference, it probably means new grades on the website
downloader.diff_two_dicts()
