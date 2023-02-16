"""Used to generate a custom code.

This script is used to generate a custom code that can be passed to
the printer script.

Each ID can be summarized in 4 segments, 3 four character segments and 1 six
character segment. For example "1100 1101 0100 001101"
"""

import argparse, re
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

def get_info_from_bits() -> tuple[str, str, str, str]:
	"""Get the code from the user """

	parser.add_argument(
		"ID",
		nargs="+",
		help="The ID to generate a code with"  # noqa
	)

	segments = parser.parse_args().ID

	# verify the segments
	if (len(segments) == 4 and len(''.join(segments)) == 18):
		if re.match('[^01]', ''.join(segments)):
			return segments

		else: 
			raise('Invalid 18 bit code') 


	elif len(segments) == 18:
		segments = (segments[0:4], segments[4:8], segments[8:12], segments[12:18])

		if re.match('[^01]', ''.join(segments)):
			return segments

		else: 
			raise('Invalid 18 bit code') 
		

	elif len(segments) > 120 and len(segments) < 140:
		rearranged = _rearrange_140_to_18(segments)
		return rearranged

	elif len(segments) > 140:
		raise('Invalid 140 bit code, too long')



def generate_printable_code():
	seg1, seg2, seg3, seg4 = _getID()

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
	parser.add_argument(
		"Type",
		dest= "type",
		choices = ["bits/barcode", "Pod Name"]
	)
	if parser.parse_args().type == "bits/barcode":
		code = get_info_from_bits()
		generate_printable_code(code)

	elif parser.parse_args().type == "Pod Name":
		# get_info_from_database()
		pass

	else:
		raise ValueError("Invalid type")
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate printable code for Nespresso Vertuo")
	multiplexer()

