"""Used to generate a custom code.

This script is used to generate a custom code that can be passed to
the printer script.

Each ID can be summarized in 4 segments, 3 four character segments and 1 six
character segment. For example "1100 1101 0100 001101"
"""
import inquirer
import re
from functools import partial

"""
The four segments are repeated four times with different separators in
between. Though the separators are the same across pods.

For example, Melozio has the following code

01 1100 10 1101 10 0100 10 010110 01
01 1100 10 1101 01 0100 01 010110 10
01 1100 01 1101 10 0100 01 010110 01
01 1100 01 1101 01 0100 01 010110 01
01 1100 01 1101 01 0100 10 010110 10
"""

def _rearrange_140_to_18(segments: str) -> tuple[str, str, str, str]:
	"""Rearrange the 140 bit code to 18 bits, removing the separator bits and getting the code for capsule"""

	splitted = segments.split("01", 1)

	code = '01' + splitted[1] + splitted[0]

	#divide into 5 groups of 28 bits
	groups = [code[i:i+28] for i in range(0, len(code), 28)]

	formatted_groups = [f'{i[0:2]} {i[2:6]} {i[6:8]} {i[8:12]} {i[12:14]} {i[14:18]} {i[18:20]} {i[20:26]} {i[26:2]}' for i in groups]

	#remove the separators
	groups_wo_separators = [re.sub(r'\s[01]{2}\s', ' ', row) for row in formatted_groups]

	if groups_wo_separators[0] == groups_wo_separators[1] == groups_wo_separators[2] == groups_wo_separators[3] == groups_wo_separators[4]:
		print(f'The code is valid, here it is: {groups_wo_separators[0][3:]}')

		return tuple(groups_wo_separators[0][3:].split())
	
	elif len(segments) < 140:
		print('The code is too short, so the code couldnt be verified')
		print('The invalid code is: ', groups_wo_separators[0].split())
	else: 
		raise Exception('Invalid 140 bit code, segments do not match')

def get_info_from_bits() -> tuple[str, str, str, str]:
	"""Get the code from the user """

	segments = input("The ID to generate a code with: ")

	# verify the segments
	if len(segments) == 4:
		if re.match('[^01]', ''.join(segments)) and len(''.join(segments)) == 18:
			return segments

		else:
			raise ValueError('Invalid 18 bit code') 


	elif len(segments) == 18:
		segments = (segments[0:4], segments[4:8], segments[8:12], segments[12:18])

		if re.match('[^01]', ''.join(segments)):
			return segments

		else: 
			raise ValueError('Invalid 18 bit code') 
		

	elif len(segments) > 120 and len(segments) <= 140:
		rearranged = _rearrange_140_to_18(segments)
		return rearranged

	elif len(segments) > 140:
		raise ValueError('Invalid 140 bit code, too long')



def generate_printable_code(code: tuple[str, str, str, str]) -> None:
	"""Generate the printable code"""

	seg1, seg2, seg3, seg4 = code

	separators = [
		['10', '10', '10', '01'],
		['10', '01', '01', '10'],
		['01', '10', '01', '01'],
		['01', '01', '01', '01'],
		['01', '01', '10', '10']
	]

	formattedCode = "" 
	for interval in range(5):

		formatter = "01{seg1}{sep1}{seg2}{sep2}{seg3}{sep3}{seg4}{sep4}"
		formatter = partial(
			formatter.format,
			seg1=seg1,
			seg2=seg2,
			seg3=seg3,
			seg4=seg4
		)

		formattedCode += formatter(
			sep1=separators[interval][0],
			sep2=separators[interval][1],
			sep3=separators[interval][2],
			sep4=separators[interval][3],
		)


	print(formattedCode)
	pass

def multiplexer():
	"""Multiplex which format is the code in. """

	  # noqa
	questions = [inquirer.List('type',
		message = "What type of code is it?",
		choices = ["bits/barcode", "Pod Name"]
	)]
	answer = inquirer.prompt(questions)

	if answer['type'] == "bits/barcode":
		code = get_info_from_bits()
		generate_printable_code(code)

	elif answer['type'] == "Pod Name":
		# get_info_from_database()
		pass

	else:
		raise ValueError("Invalid type")
	
if __name__ == "__main__":
	print("Generate printable code for Nespresso Vertuo")
	multiplexer()

