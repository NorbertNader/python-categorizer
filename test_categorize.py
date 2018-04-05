"""Test Categorize module

"""

import unittest
import os.path
from categorize import Categorize

class CategorizeTest(unittest.TestCase):
    """Test class for Categorize class

    """

    # mock data with duplicate buckets and expect to filter out duplicates
    mock_data_duplicate_buckets = {
        'buckets': [
            {'publisher': 'test', 'price': '1', 'duraion': '1_day'},
            {'publisher': 'test', 'price': '1', 'duraion': '1_day'},
            {'publisher': 'test', 'price': '1', 'duraion': '8_days'}
        ],
        'expected': [
            {
                'bucket': 'test,1,1_day',
                'purchases': []
            },
            {
                'bucket': 'test,1,8_days',
                'purchases': []
            }
        ]
    }
    # mock data where the number of matching attributes overweighs
    mock_data_weight_on_number_of_mathces = {
        'buckets': [
            {'publisher': 'test', 'price': '1', 'duraion': '1_day'},
            {'publisher': 'test', 'price': '1', 'duraion': '8_days'}
        ],
        'purchases': [
            '99162,1150783559734,test,AUS,1,1_day,2017-01-10 08:33:13.570609',
            '99162,1150783559734,test,AUS,1,8_day,2017-07-22 15:29:11.578183'
        ],
        'expected': [
            {
                'bucket': '*,*,*',
                'purchases': []
            },
            {
                'bucket': 'test,1,1_day',
                'purchases': [
                    '99162,1150783559734,test,AUS,1,1_day,2017-01-10 08:33:13.570609'
                ]
            },
            {
                'bucket': 'test,1,8_day',
                'purchases': [
                    '99162,1150783559734,test,AUS,1,8_day,2017-07-22 15:29:11.578183'
                ]
            }
        ]
    }
    # mock data where attribute with bigger wieght overweighs
    mock_data_wieght_on_attribute = {
        'buckets': [
            {'publisher': 'test', 'price': '1', 'duraion': '*'},
            {'publisher': 'test2', 'price': '1', 'duraion': '*'}
        ],
        'purchases': [
            '99162,1150783559734,test,AUS,1,1_day,2017-01-10 08:33:13.570609',
            '99162,1150783559734,test2,AUS,1,8_day,2017-07-22 15:29:11.578183'
        ],
        'expected': [
            {
                'bucket': '*,*,*',
                'purchases': []
            },
            {
                'bucket': 'test,1,*',
                'purchases': [
                    '99162,1150783559734,test,AUS,1,1_day,2017-01-10 08:33:13.570609'
                ]
            },
            {
                'bucket': 'test2,1,*',
                'purchases': [
                    '99162,1150783559734,test2,AUS,1,1_day,2017-07-22 15:29:11.578183'
                ]
            }
        ]
    }
    # mock data where does not match any so goes to wildcard
    mock_data_wieght_on_attribute = {
        'buckets': [
            {'publisher': 'test', 'price': '1', 'duraion': '*'},
        ],
        'purchases': [
            '99162,1150783559734,test2,AUS,2,2_day,2017-01-10 08:33:13.570609'
        ],
        'expected': [
            {
                'bucket': '*,*,*',
                'purchases': [
                    '99162,1150783559734,test2,AUS,2,2_day,2017-01-10 08:33:13.570609'
                ]
            },
            {
                'bucket': 'test,1,*',
                'purchases': []
            }
        ]
    }

    def setUp(self):
        """Create instance of Categorize object

        """
        self.cat = Categorize()

    def test_files_exist(self):
        """Test if input files for buckets and purchases exist

        """
        is_file_buckets = os.path.isfile(self.cat.buckets_csv)
        self.assertTrue(is_file_buckets, 'buckets file does not exist')

        is_file_purchases = os.path.isfile(self.cat.purchases_csv)
        self.assertTrue(is_file_purchases, 'purchases file does not exist')

if __name__ == '__main__':
    unittest.main()
