#unit testing for dictionary program
import unittest
from final import get_url
from final import find_matches
from final import getchoice
from final import select_match

class mytest(unittest.TestCase):
	def Test_get_url(self):  #test the geturl method
		self.assertEqual(get_url(),'item')
	
	def Test_find_matches(self): #tests the list of matches 
		self.assertEqual(find_matches('description'),'Latest scores from Cricinfo')
		self.assertEqual(find_matches('title'),'Cricinfo Live Scores')
	
	
	def Test_select_match(self):  #test the operation on selecting a match
		self.assertEqual(select_match(),1)
		self.assertEqual(select_match(),2)
		self.assertEqual(select_match(),3)
		self.assertEqual(select_match(),100)
		self.assertEqual(select_match(),yes)
	
	def Test_signal_handler(self):
		self.assertEqual(signal_handler(),'')

Unittest.main()
