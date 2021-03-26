from serverapi import ServerApi
# from Common import *
# from util import json_schema_check
import data.login as login
import data.url_extension as url_ext
import util
from parameterized import parameterized, parameterized_class
import random

# verify that user can login
# store accessToken in global variable
def test_post_sign_in():
    API_URL = "{}/{}".format(login.API_URL,url_ext.SIGN_IN)
    client = ServerApi(api_url=API_URL)
    response = client.post_without_bearer_token(
                            {
                                "email": login.EMAIL,
                                "emailVerifier": login.EMAILVERIFIER,
                                "domain": login.DOMAIN
                            }
                        )
    assert response.status_code == 200
    login.ACCESS_TOKEN = response.json()['accessToken']
    
# verify the following
# - eq5d can be drafted
# - eq5d can be created
# - fim can be drafted
# - fim can be created
# - stroke111 can be drafted can created
def test_post_create_section_3_mbi_stroke():
    response_caresetting_create = util.section_1_2_flow()

    # EQ5D draft admission
    response_eq5d_draft_admission = util.eq5d_flow(
                                        caresetting_date_assessed = response_caresetting_create['dateOfAdmission'],
                                        caresetting_id = response_caresetting_create['id'],
                                        type = 'A',
                                        assessment_id = None,
                                        is_draft = True
                                    )
    # Assessment EQ5D
    response_assessment = util.assessment_flow(
                                    assessment_category = 'EQ5D', 
                                    assessment_id = response_eq5d_draft_admission.json()['assessmentId']
                                )
    
    response_eq5d_draft_admission = response_eq5d_draft_admission.json()
    response_assessment = response_assessment.json()

    util.assert_eq5d(response_eq5d_draft_admission,response_assessment)

    # EQ5D create admission
    response_eq5d_create_admission = util.eq5d_flow(
                                        caresetting_date_assessed = response_caresetting_create['dateOfAdmission'],
                                        caresetting_id = response_caresetting_create['id'],
                                        type = 'A',
                                        assessment_id = response_eq5d_draft_admission['assessmentId'],
                                        assessed_by = response_eq5d_draft_admission['assessedby'],
                                        is_draft = False
                                    )
    # Assessment EQ5D
    response_assessment_2 = util.assessment_flow(
                                    assessment_category = 'EQ5D', 
                                    assessment_id = response_eq5d_draft_admission['assessmentId']
                                )
    
    response_eq5d_create_admission = response_eq5d_create_admission.json()
    response_assessment_2 = response_assessment_2.json()

    util.assert_eq5d(response_eq5d_create_admission,response_assessment_2)


    # MBI draft admission
    response_mbi_draft_admission = util.mbi_flow(
                                        caresetting_date_assessed = response_caresetting_create['dateOfAdmission'],
                                        caresetting_id = response_caresetting_create['id'],
                                        type = 'A',
                                        assessment_id = None,
                                        is_draft = True
                                    )
    # Assessment FIM
    response_assessment_3 = util.assessment_flow(
                                    assessment_category = 'MBI', 
                                    assessment_id = response_mbi_draft_admission.json()['assessmentId']
                                )
    
    response_mbi_draft_admission = response_mbi_draft_admission.json()
    response_assessment_3 = response_assessment_3.json()

    print(response_mbi_draft_admission)
    print(response_assessment_3)
    
    util.assert_mbi(response_mbi_draft_admission,response_assessment_3)

    # # FIM create admission
    # response_fim_create_admission = util.fim_flow(
    #                                     caresetting_date_assessed = response_caresetting_create['dateOfAdmission'],
    #                                     caresetting_id = response_caresetting_create['id'],
    #                                     type = 'A',
    #                                     assessment_id = None,
    #                                     is_draft = False
    #                                 )
    # # Assessment FIM
    # response_assessment_4 = util.assessment_flow(
    #                                 assessment_category = 'FIM', 
    #                                 assessment_id = response_fim_create_admission.json()['assessmentId']
    #                             )
    
    # response_fim_create_admission = response_fim_create_admission.json()
    # response_assessment_4 = response_assessment_4.json()

    # util.assert_fim(response_fim_create_admission,response_assessment_4)
    