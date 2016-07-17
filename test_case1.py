#unit testing for dictionary program
import unittest
from final import get_url
from final import find_matches
from final import getchoice
from final import select_match



class mytest(unittest.TestCase):

	
	
	def test_get_choice(self):
		self.assertEqual(type(getchoice()),int)
		

	def test_select_match(self):
		self.assertEqual(type(select_match()),int)
		

unittest.main()
