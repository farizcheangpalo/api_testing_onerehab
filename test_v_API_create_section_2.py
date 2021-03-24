from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login as login
import data.url_extension as url_ext
import util
from parameterized import parameterized, parameterized_class
import random

# verify that create section 2 is correct
# a random correct format is created
def test_post_create_section_2():
    # Create 1a
    response = util.create_flow()
    # Search
    patient_id = util.search_flow(response.json())
    # Create 1b
    response_section_1b = util.socialmed_create_flow(patient_id)
    # Episode listing
    response_episode_listing = util.episode_listing_flow(patient_id)
    # Social Med
    response_social_med = util.social_med_flow(response_episode_listing.json()['episodes'][0]['id'])
    # Care Setting Active
    response_caresetting_active = util.caresetting_active_flow(response_episode_listing.json()['episodes'][0]['id'])
    # Create Care Setting (Section 2)
    response_caresetting_create = util.caresetting_create_flow(
            patient_id=patient_id,
            episode_id=response_episode_listing.json()['episodes'][0]['id'],
            status=response_episode_listing.json()['episodes'][0]['status']
        )
    # Episode listing
    response_episode_listing_2 = util.episode_listing_flow(patient_id)

    response_section_1b = response_section_1b.json()
    response_episode_listing = response_episode_listing.json()
    response_social_med = response_social_med.json()
    response_caresetting_create = response_caresetting_create.json()
    response_episode_listing_2 = response_episode_listing_2.json()

    # print(response_section_1b)
    # print(response_episode_listing)
    # print(response_social_med)
    # print(response_caresetting_active)
    print(response_caresetting_create)
    print(response_episode_listing_2)

    # Verification
    assert response_section_1b['episodeId'] == response_episode_listing['episodes'][0]['id']
    assert response_section_1b['rdgPrimary'] == response_episode_listing['episodes'][0]['rdg']
    assert "Active" == response_episode_listing['episodes'][0]['status']

    # remove the fields that make them different
    del response_section_1b['episodeId']
    del response_social_med['employmentStatus']
    assert response_section_1b == response_social_med

    assert response_caresetting_active.text == 'false'

    assert response_caresetting_create['id'] == response_episode_listing_2['episodes'][0]['careSettings'][0]['id']
    assert response_caresetting_create['organizationCenter'] == response_episode_listing_2['episodes'][0]['careSettings'][0]['careProviderName']
    assert response_caresetting_create['status'] == response_episode_listing_2['episodes'][0]['careSettings'][0]['status']
    assert response_caresetting_create['dateOfAdmission'] == response_episode_listing_2['episodes'][0]['careSettings'][0]['dateOfAdmission']
    assert response_caresetting_create['settingClassification'] == response_episode_listing_2['episodes'][0]['careSettings'][0]['settingClassification']
    # assert response_caresetting_create['relevantMedicalHistory'] == 
    # assert response_caresetting_create['caregiverStatusOnAdmission'] == 
    # assert response_caresetting_create['relationshipOfPrimaryCaregiver'] == 
    # assert response_caresetting_create['sftpCreated'] == 
    




