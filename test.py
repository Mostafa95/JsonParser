import unittest
import jsonparse as jparse
#import jparse as jp

class Test(unittest.TestCase):
    
    def readFile(self,path):
        with open(path,"r") as f:
            content = f.read()
        return content
    
    def test_step1_invalid(self):
        invalidPath = 'tests/step1/invalid.json'
        content = self.readFile(invalidPath)
        ans = 'Invalid token structure.'
        with self.assertRaises(Exception) as context:
            jparse.from_string(content)
        self.assertEqual(str(context.exception), ans)
        
    def test_step1_valid(self):
        validPath = 'tests/step1/valid.json'
        content = self.readFile(validPath)
        self.assertEqual(jparse.from_string(content),{})
    
    def test_step2_invalid(self):
        validPath = 'tests/step2/invalid.json'
        content = self.readFile(validPath)
        ans= 'Unexpected token in object: }'
        with self.assertRaises(ValueError) as context:
            jparse.from_string(content)
        self.assertEqual(str(context.exception), ans)    
        
    def test_step2_invalid2(self):
        validPath = 'tests/step2/invalid2.json'
        content = self.readFile(validPath)
        ans = 'Invalid character at ind 22 , k'
        with self.assertRaises(Exception) as context:
            jparse.from_string(content)
        self.assertEqual(str(context.exception),ans)
        
    def test_step2_valid(self):
        validPath = 'tests/step2/valid.json'
        content = self.readFile(validPath)
        self.assertEqual(jparse.from_string(content),{"key": "value"})
        
    def test_step2_valid2(self):
        validPath = 'tests/step2/valid2.json'
        content = self.readFile(validPath)
        self.assertEqual(jparse.from_string(content),{"key": "value","key2": "value"})
    
    def test_step3_invalid(self):
        validPath = 'tests/step3/invalid.json'
        content = self.readFile(validPath)
        ans = 'Invalid character at ind 28 , F'
        with self.assertRaises(Exception) as context:
            jparse.from_string(content)
        self.assertEqual(str(context.exception), ans)
        
    def test_step3_valid(self):
        validPath = 'tests/step3/valid.json'
        content = self.readFile(validPath)
        self.assertEqual(jparse.from_string(content),{"key1": True,"key2": False,"key3": None,"key4": "value","key5": 101})
    
    def test_step4_invalid(self):
        validPath = 'tests/step4/invalid.json'
        content = self.readFile(validPath)
        ans = 'Invalid character at ind 97 , \''
        with self.assertRaises(Exception) as context:
            jparse.from_string(content)
        self.assertEqual(str(context.exception), ans)
    
    def test_step4_valid(self):
        validPath = 'tests/step4/valid.json'
        ans = {\
            "key": "value",\
            "key-n": 101,\
            "key-o": {},\
            "key-l": []\
        }
        content = self.readFile(validPath)
        self.assertEqual(jparse.from_string(content),ans)
    
    def test_step4_valid2(self):
        validPath = 'tests/step4/valid2.json'
        ans = {\
            "key": "value",\
            "key-n": 101,\
            "key-o": {\
                "inner key": "inner value"\
            },\
            "key-l": ["list value"]\
            }
        content = self.readFile(validPath)
        self.assertEqual(jparse.from_string(content),ans)
          
if __name__ == '__main__':
    unittest.main()