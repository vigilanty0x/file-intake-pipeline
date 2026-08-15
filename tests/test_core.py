import unittest
from file_intake_pipeline import intake,probe
F={"name":"a.txt","size":2,"sha256":"a"*64,"media_type":"text/plain"}
class Tests(unittest.TestCase):
 def test_accept(self): self.assertTrue(intake([F])["accepted"])
 def test_traversal(self): self.assertFalse(intake([{**F,"name":"../x"}])["accepted"])
 def test_duplicate(self): self.assertFalse(intake([F,F])["accepted"])
 def test_probe(self): self.assertTrue(probe()["ok"])
if __name__=="__main__": unittest.main()
