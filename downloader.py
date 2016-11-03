from urllib.request import urlopen
import json

'''
This method downloads a webpage from a given URL
and returns its contents (HTML source code)
'''
def download_webpage(url):
	print("Downloading {0} ...".format(url))
	html = urlopen(url)
	content = html.read().decode("utf-8")

	return content


'''
Given a HTML table, extract from every header and row
the contents of the table.
Then, enters this information in a dictionary, in which the key
is the filename and the value is a tuple
in the format (last_modified_date, file_size)
'''
def extract_table_data(table):
	rows = table.findChildren(['th', 'tr'])

	dict_files = {}
	for row in rows:
		cells = row.findChildren('td')

		if(len(cells) >= 5):
			file_link = cells[1].string		#file_link = cells[1].a["href"]
			last_modified = cells[2].string
			file_size = cells[3].string
			#print("{0} - {1} - {2}\n".format(file_link, last_modified, file_size))

			dict_files[file_link] = (last_modified, file_size)

	#for key in dict_files.keys():
		#print("{0}: {1}".format(key, dict_files[key]))

	return dict_files

'''
	Saves the original dictionary to a json file.
	This file will then be compared to newer versions, in search of differences.
'''
def save_dict_to_json(dict, filename):
	with open(filename, "w") as fp:
		json.dump(dict, fp, sort_keys=True, indent=4)
		
		if(fp != None):
			print("Successfully saved to {0}".format(filename))
		else:
			print("Something wrong happened while creating {0}".format(filename))


'''
This method compares two dictionaries: the original one and the newer one,
and check if there are any differences between their contents. 
It assumes that the keys are the same.
TODO: one dict might have more keys than the other, so I have to check that...
'''
def diff_two_dicts():
	diff_found = False

	with open('original_data.json', 'r') as fp1:
		original_data = json.load(fp1)
	with open('new_data.json', 'r') as fp2:
		new_data = json.load(fp2)

	for key in original_data.keys():
		if(original_data[key] != new_data[key]):
			diff_found = True
			print("DIFFERENCE FOUND BETWEEN VERSIONS!")
			print("Original version: {0} : {1}".format(key, original_data[key]))
			print("New version: {0} : {1}".format(key, new_data[key]))

	if(diff_found == False):
		print("No new version found, apparently :(\nCheck again later...")

		#print(key, original_data[key])
