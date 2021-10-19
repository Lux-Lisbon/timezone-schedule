import unittest
from main import *


class UnitTests(unittest.TestCase):

  def test_printEntry(self):
      self.assertEquals(printEntry(timezoneMenu), timezoneVar.get())

