from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login as login
import data.url_extension as url_ext
import util
from parameterized import parameterized, parameterized_class

# verify that patients sorted by full name in ascending
def test_post_sort_by_full_name_asc():
    util.assert_sort_by(list=login.ACTIVE_LIST_ITEMS, type='active', sort_by=login.SORT_BY['fullname_asc'], is_asc=True, field='fullName')

# verify that patients sorted by full name in descending
def test_post_sort_by_full_name_desc():
    util.assert_sort_by(list=login.DISCHARGED_LIST_ITEMS, type='discharged', sort_by=login.SORT_BY['fullname_desc'], is_asc=False, field='fullName')
    
# verify that patients sorted by date of birth in ascending
def test_post_sort_by_date_of_birth_asc():
    util.assert_sort_by(list=login.ACTIVE_LIST_ITEMS, type='active', sort_by=login.SORT_BY['dateofbirth_asc'], is_asc=True, field='dateofBirth')

# verify that patients sorted by date of birth in descending
def test_post_sort_by_date_of_birth_desc():
    util.assert_sort_by(list=login.DISCHARGED_LIST_ITEMS, type='discharged', sort_by=login.SORT_BY['dateofbirth_desc'], is_asc=False, field='dateofBirth')

# verify that patients sorted by date of birth in ascending
def test_post_sort_by_nric_asc():
    util.assert_sort_by(list=login.ACTIVE_LIST_ITEMS, type='active', sort_by=login.SORT_BY['nric_asc'], is_asc=True, field='nric')

# verify that patients sorted by date of birth in descending
def test_post_sort_by_nric_desc():
    util.assert_sort_by(list=login.DISCHARGED_LIST_ITEMS, type='discharged', sort_by=login.SORT_BY['nric_desc'], is_asc=False, field='nric')
