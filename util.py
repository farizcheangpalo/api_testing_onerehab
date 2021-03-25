import string
import random
from requests import Response
# from json import JSONDecodeError
from jsonschema import validate, SchemaError, ValidationError
import json
from serverapi import ServerApi
import data.login as login
import data.url_extension as url_ext
import datetime
import names

def print_pass_message(text=''):
    return print("\033[1;32;40m"+text)

def print_fail_message(text=''):
    return print("\033[1;31;40m"+text)

def r_lum():
    num = str(int(random.random()*10))
    if num == "":
        return 0
    else:
        return int(num)

def generate_nric():
    str_digit = ""
    random_num = 0
    first_letter = random.choice('STGF')
    if first_letter == 'S' or first_letter == 'T':
        last_letter = ['J','Z','I','H','G','F','E','D','C','B','A']
    else:
        last_letter = ['X','W','U','T','R','Q','P','N','M','L','K']
    if first_letter == 'T' or first_letter == 'G':   
        random_num = 4
    else:
        random_num = 0
    for i in [2,7,6,5,4,3,2]:
        digit = r_lum()
        random_num = random_num + i * digit
        str_digit = str_digit + str(digit)
    last_letter = last_letter[random_num%11]
    return first_letter + str_digit + last_letter

def generate_dob(age=50):
    today = datetime.date.today()
    month = datetime.date.today().month
    day = datetime.date.today().day
    if str(month)=="2" and str(day)=="29":
        year = str(today).split("-")[0]
        birth_year = str(int(year) - age)
        dob = str(today).replace(year,birth_year)
        dob = str(today)[:8] + "28"
        return dob
    else:
        year = str(today).split("-")[0]
        birth_year = str(int(year) - age)
        dob = str(today).replace(year,birth_year)
        return dob

def generate_date(days=20):
    today = datetime.date.today()
    month = datetime.date.today().month
    day = datetime.date.today().day
    # yesterday = today - datetime.timedelta(days = 1)
    return str(today - datetime.timedelta(days = days))

# Get the date difference between the first and last date
def get_num_of_days_between_date(first_date='',last_date=''):
    arr_first_date = first_date.split('-')
    arr_last_date = last_date.split('-')
    f_date = datetime.date(int(arr_first_date[0]), int(arr_first_date[1]), int(arr_first_date[2]))
    l_date = datetime.date(int(arr_last_date[0]), int(arr_last_date[1]), int(arr_last_date[2]))
    delta = l_date - f_date
    return str(delta.days).split(" ")[0]

def sort_field_by(list={},field='',is_asc=True,page_size=20):
    arr = []
    for item in list:
        arr.append(item[field])
    
    if not field == 'fullName':
        if is_asc:
            arr.sort(reverse=False)
        else:
            arr.sort(reverse=True)
        return arr[:page_size]
    else:
        if not is_asc:
            arr.reverse()
        return arr[:page_size]

def store_response_sort_by(list={},field=''):
    arr = []
    for item in list:
        arr.append(item[field])
    return arr

def assert_sort_by(list={}, type='active', sort_by='', is_asc=True, field=''):
    API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
    client = ServerApi(api_url=API_URL)
    request_json = read_json_file("data/json/request/{}_list.json".format(type))

    details = get_details_after_login(login.EMAIL,login.DOMAIN)
    request_json['organization'] = details['orgCenterResponseCode']
    request_json['sortBy'] = [sort_by]
    response = client.post_with_bearer_token(request_json)
    
    assert response.status_code == 200

    fullname_arr = store_response_sort_by(response.json()["items"],field=field)
    expected_arr = sort_field_by(list=list,field=field,is_asc=is_asc,page_size=request_json['pageSize'])
    
    print(fullname_arr)
    print(expected_arr)
    assert fullname_arr == expected_arr

def get_details_after_login(email=None, domain=None, subdomain=None):
    if email=="admincsp" and domain=="healthgrp" and subdomain==None:
        return {
                    "userId": "e8c95a8e49aa4e968e7327ff85b1c419",
                    "subOrgResponseName": "OneRehab CSP",
                    "subOrgResponseCode": "OneRehab_CSP",
                    "orgCenterResponseName": "OneRehab-CSP-Center",
                    "orgCenterResponseCode": "OneRehab_CSP_Center"
                }

def read_json_file(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def get_all_active_list(total_page=None):
    login.ACTIVE_LIST_ITEMS = []
    details = get_details_after_login(login.EMAIL,login.DOMAIN)
    for i in range(total_page):
        API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
        client = ServerApi(api_url=API_URL)
        request_json = read_json_file("data/json/request/active_list.json")
        request_json['organization'] = details['orgCenterResponseCode']
        request_json['page'] = i+1

        response = client.post_with_bearer_token(request_json)

        for item in response.json()['items']:
            login.ACTIVE_LIST_ITEMS.append(item)

    return login.ACTIVE_LIST_ITEMS

def get_all_discharged_list(total_page=None):
    login.DISCHARGED_LIST_ITEMS = []
    details = get_details_after_login(login.EMAIL,login.DOMAIN)
    for i in range(total_page):
        API_URL = "{}/{}".format(login.API_URL,url_ext.LIST)
        client = ServerApi(api_url=API_URL)
        request_json = read_json_file("data/json/request/discharged_list.json")
        request_json['organization'] = details['orgCenterResponseCode']
        request_json['page'] = i+1

        response = client.post_with_bearer_token(request_json)

        for item in response.json()['items']:
            login.DISCHARGED_LIST_ITEMS.append(item)

    return login.DISCHARGED_LIST_ITEMS

def create_patient_1a(details={}):
    return {
        "fullName": names.get_full_name(gender=random.choice(["male", "female"])),
        "nric": generate_nric(),
        "identificationType": random.choice(["SP", "SB", "F", "NA"]),
        "dateofBirth": generate_dob(random.randint(1,100)),
        "gender": random.choice(["M", "F"]),
        "race": random.choice(["C", "M", "I", "O"]),
        "address": "59 Tuas South Ave 1 Singapore",
        "postalCode": generate_postalcode(),
        "organizationCenter": details['orgCenterResponseCode']
    }

def create_patient_1b(details={}, custom_dict={}, patient_id=''):
    if not custom_dict:
        employment_status = random.choice(["E", "U", "SE", "H", "R", "O"])
        lift_landing = random.choice(["Y", "N"])
        if lift_landing == "N":
            lift_landing_flights = random.choice(["OneFlight", "OneFlight", "OneFlight", "OTHERS"])
            if lift_landing_flights == "OTHERS":
                lift_landing_flight_others_comments = "Balcony"
            else:
                lift_landing_flight_others_comments = ""
        else:
            lift_landing_flights = ""
            lift_landing_flight_others_comments = ""

        presence_of_steps = random.choice([True, False])
        if presence_of_steps:
            location_of_steps = multiple_choice(["OME", "OT", "O"])
            arr_location_of_steps = location_of_steps.split(',')
            if "O" in arr_location_of_steps:
                number_of_steps_other_location = str(random.randint(1,1000))
                location_of_steps_comments = "It is very steep"
            else:
                number_of_steps_other_location = ""
                location_of_steps_comments = ""
            if "OME" in arr_location_of_steps:
                number_of_steps_outside_main_entry = str(random.randint(1,1000))
            else:
                number_of_steps_outside_main_entry = ""
            if "OT" in arr_location_of_steps:
                number_of_steps_outside_toilet = str(random.randint(1,1000))
            else:
                number_of_steps_outside_toilet = ""
        else:
            number_of_steps_outside_main_entry = ""
            number_of_steps_outside_toilet = ""
            number_of_steps_other_location = ""
            location_of_steps = ""
            location_of_steps_comments = ""

        kerb = random.choice(["Y", "N"])
        referring_institution = "Singapore General Hospital"
        referral_source_setting = random.choice(["AHI", "ED", "SOC", "CHI", "RDCSCCAAH", "PC", "GP", "NH", "SAC", "WISR", "OTHER"])
        if referral_source_setting == "OTHER":
            referral_source_setting_other = "Referral Patient"
        else:
            referral_source_setting_other = ""
        premorbid_BADL_status = [multiple_choice(["IIBADLS", "NAIBADLS", "DIBADLS", "O"])]
        premorbid_IADL_status = [multiple_choice(["NAIIADLS", "IIIADLS", "O"])]
        premorbid_mobility_status_comm = random.choice(["WID", "WIIM", "WAD", "WAI", "WANA", "NIP", "NAP", "H"])
        if not premorbid_mobility_status_comm == "H":
            premorbid_use_of_mobility_aid = multiple_choice(["N", "U", "WS", "NBQS", "BBQS", "C", "WF", "RF", "WC", "MW", "MS", "O"])
        else:
            premorbid_use_of_mobility_aid = ""
        premorbid_mobility_status_home = random.choice(["WI", "WA", "NIP", "NAP", "B", "O"])
        if not premorbid_mobility_status_home == "B":
            premorbid_mobility_aids_home = multiple_choice(["N", "F", "U", "WS", "NBQS", "BBQS", "C", "WF", "RF", "WC", "MW", "MS", "O"])
        else:
            premorbid_mobility_aids_home = ""
        rdg_primary =    random.choice([  
                            "Stroke111", "Stroke112", "Stroke113", "Stroke121", "Stroke122", "Stroke123",
                            "SCI211", "SCI212", "SCI221", "SCI222", "SCI231",
                            "HIP311", "HIP312", "HIP313",
                            "AMP411", "AMP412", "AMP413", "AMP414", "AMP421", "AMP422", "AMP423", "AMP424",
                            "MSK511", "MSK512", "MSK513", "MSK521",
                            "DECON61", "DECON62", "DECON63"
                        ])
        if rdg_primary == "DECON63":
            rdg_primary_frailty = multiple_choice(["CFS", "FI", "FFC", "O"])

        else:
            rdg_primary_frailty = ""

        dict = {
                    "employmentStatus": employment_status,
                    "liftLandingFlights": lift_landing_flights,
                    "liftLanding": lift_landing,
                    "locationOfSteps": location_of_steps,
                    "presenceOfSteps": presence_of_steps,
                    "kerb": kerb,
                    "referringInstitution": referring_institution,
                    "referralSourceSetting": referral_source_setting,
                    "premorbidBADLStatus": premorbid_BADL_status,
                    "premorbidIADLStatus": premorbid_IADL_status,
                    "premorbidMobilityStatusComm": premorbid_mobility_status_comm,
                    "rdgPrimary": rdg_primary,
                    # "rdgSecondary1": "Stroke111",
                    # "rdgSecondary2": "Stroke112",
                    # "rdgSecondary3": "Stroke123",
                    # "rdgSecondary4": "SCI221",
                    # "rdgSecondary5": "SCI211",
                    "liftLandingFlightOthersComments": lift_landing_flight_others_comments,
                    "numberOfStepsOutsideMainEntry": number_of_steps_outside_main_entry,
                    "numberOfStepsOutsideToilet": number_of_steps_outside_toilet,
                    "numberOfStepsOtherLocation": number_of_steps_other_location,
                    "locationOfStepsComments": location_of_steps_comments,
                    "premorbidUseOfMobilityAid": premorbid_use_of_mobility_aid,
                    "premorbidMobilityStatusHome": premorbid_mobility_status_home,
                    "premorbidMobilityAidsHome": premorbid_mobility_aids_home,
                    "referralSourceSettingOther": referral_source_setting_other,
                    "rdgPrimaryFrailty": rdg_primary_frailty,
                    "patientId": patient_id,

                    "organizationCenter": details["orgCenterResponseCode"]


                }
    else:
        custom_dict["organizationCenter"] = details["orgCenterResponseCode"]
        custom_dict["patientId"] = patient_id
        dict = custom_dict
        
    return dict

def create_caresetting(details={}, custom_dict={}, patient_id='', episode_id='', status=''):
    if not custom_dict:
        date_of_admission = generate_date(random.randint(10,100))
        setting_name = details["orgCenterResponseName"]
        # setting_classification = random.choice(["AHI", "AHAHP", "CHI", "DRC", "SCC", "AAH", "PC", "HHSHT", "NH"])
        setting_classification = "SCC"
        relevant_medical_history = "Test Relevant Medical History"
        caregiver_status_on_admission = random.choice(["D", "NLC", "NAC", "NNC", "NA"])
        if caregiver_status_on_admission == "NAC" or caregiver_status_on_admission == "NLC":
            relationship_of_primary_caregiver = random.choice(["SE", "N", "S", "C", "CI", "P", "SI", "GC", "DH", "O"])
        else:
            relationship_of_primary_caregiver = ""

        
        dict = {
            "dateOfAdmission": date_of_admission,
            "settingName": setting_name,
            "settingClassification": setting_classification,
            "relevantMedicalHistory": relevant_medical_history,
            "caregiverStatusOnAdmission": caregiver_status_on_admission,
            "relationshipOfPrimaryCaregiver": relationship_of_primary_caregiver,
            "organizationCenter": details["orgCenterResponseCode"],
            "episodeId":  episode_id,
            "status": status,
            "patientId": patient_id
        }
    else:
        custom_dict["organizationCenter"] = details["orgCenterResponseCode"]
        custom_dict["patientId"] = patient_id
        custom_dict["episodeId"] = episode_id
        custom_dict["settingName"] = details["orgCenterResponseName"]
        dict = custom_dict
    return dict

def create_draft_eq5d(details={}, custom_dict={}, caresetting_date_assessed = '', caresetting_id='', status='Draft', assessment_id=None, type='A', assessed_by=None):
    if not custom_dict:
        mobility = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE"])
        self_care = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE"])
        usual_activites = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE"])
        pain_or_discomfort = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE"])
        anxiety_depression = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE"])
        rate_health = str(random.randint(0,100))

        dict = {
            "dateAssessed": caresetting_date_assessed,
            "mobility": mobility,
            "selfCare": self_care,
            "usualActivities": usual_activites,
            "painOrDiscomfort": pain_or_discomfort,
            "anxietyDepression": anxiety_depression,
            "rateHealth": rate_health,
            "careSettingId": caresetting_id,
            "assessmentFormStatus": status,
            "assessmentId": assessment_id,
            "assessmentType": type,
            "organizationCenter": details["orgCenterResponseCode"]
        }

        if not assessed_by==None:
            dict['assessedby'] = assessed_by
    else:
        custom_dict["organizationCenter"] = details["orgCenterResponseCode"]
        custom_dict["careSettingId"] = caresetting_id
        custom_dict["assessmentId"] = assessment_id
        dict = custom_dict
    return dict

def create_draft_fim(details={}, custom_dict={}, caresetting_date_assessed = '', caresetting_id='', status='Draft', assessment_id=None, type='A', assessed_by=None):
    if not custom_dict:
        score_dict =    {
                            "ONE": 1,
                            "TWO": 2,
                            "THREE": 3,
                            "FOUR": 4,
                            "FIVE": 5,
                            "SIX": 6,
                            "SEVEN": 7
                        }

        eating = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        grooming = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        fimbathing = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        bathing = fimbathing
        dressing_upper = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        dressing_lower = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        toileting = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        bladder = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        bowel = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        transfer = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        transfer_toilet = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        transfer_bath = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        locomotion_type = random.choice(["W", "WH", "B"])
        if locomotion_type == "W":
            locomotion_walk = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
            locomotion_wheelchair = ""
            locomotion_both = ""
            locomotion = locomotion_walk
        elif locomotion_type == "WH":
            locomotion_wheelchair = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
            locomotion_walk = ""
            locomotion_both = ""
            locomotion = locomotion_wheelchair
        elif locomotion_type == "B":
            locomotion_both = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
            locomotion_wheelchair = ""
            locomotion_walk = ""
            locomotion = locomotion_both
        stairs = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])

        print(locomotion)
        motor_sub_score =   score_dict[eating] + \
                            score_dict[grooming] + \
                            score_dict[fimbathing] + \
                            score_dict[dressing_upper] + \
                            score_dict[dressing_lower] + \
                            score_dict[toileting] + \
                            score_dict[bladder] + \
                            score_dict[bowel] + \
                            score_dict[transfer] + \
                            score_dict[transfer_toilet] + \
                            score_dict[transfer_bath] + \
                            score_dict[locomotion] + \
                            score_dict[stairs]

        comprehension_category = random.choice(["V", "NV", "BOTH"])
        comprehension = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        expression_category = random.choice(["V", "NV", "BOTH"])
        expression = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        social_interaction = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        problem_solving = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        memory = random.choice(["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN"])
        
        cognitive_sub_score =   score_dict[comprehension] + \
                                score_dict[expression] + \
                                score_dict[social_interaction] + \
                                score_dict[problem_solving] + \
                                score_dict[memory]

        total_fim_score = motor_sub_score + cognitive_sub_score
        total_score = total_fim_score
        
        form_version = "V1"
        
        dict = {
            "dateAssessed": caresetting_date_assessed,
            "eating": eating,
            "grooming": grooming,
            "fimbathing": fimbathing,
            "dressingUpper": dressing_upper,
            "dressingLower": dressing_lower,
            "toileting": toileting,
            "bladder": bladder,
            "bowel": bowel,
            "transfer": transfer,
            "transferToilet": transfer_toilet,
            "transferBath": transfer_bath,
            "locomotionType": locomotion_type,
            "stairs": stairs,
            "motorSubScore": motor_sub_score,
            "comprehensionCategory": comprehension_category,
            "comprehension": comprehension,
            "expressionCategory": expression_category,
            "expression": expression,
            "socialInteraction": social_interaction,
            "problemSolving": problem_solving,
            "memory": memory,
            "cognitiveSubScore": cognitive_sub_score,
            "totalFimScore": total_fim_score,
            "locomotionWalk": locomotion_walk,
            "locomotionWheelchair": locomotion_wheelchair,
            "locomotionBoth": locomotion_both,
            "careSettingId": caresetting_id,
            "formVersion": form_version,
            "assessmentType": type,
            "assessmentFormStatus": status,
            "bathing": bathing,
            "totalScore": total_score,
            "assessmentId": assessment_id,
            "organizationCenter": details["orgCenterResponseCode"]
        }

        if not assessed_by==None:
            dict['assessedby'] = assessed_by
    else:
        custom_dict["organizationCenter"] = details["orgCenterResponseCode"]
        custom_dict["careSettingId"] = caresetting_id
        custom_dict["assessmentId"] = assessment_id
        dict = custom_dict

    return dict

def generate_string(num_char=255):
    string = ''
    for i in range(num_char):
        string = string + 'y'
    return encode_64(string)

def generate_postalcode():
    postal_code = ''
    for _ in range(6):
        postal_code += str(int(random.random() * 10))
    return postal_code

def encode_64(message=""):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return str(base64_message)

def multiple_choice(arr=[]):
    new_arr = random.choices(arr, k=len(arr))
    final_arr = []
    # remove duplicates
    for num in new_arr:
        if num not in final_arr:
            final_arr.append(num)
    return ",".join(final_arr)

def search_flow(resp=[]):
    API_URL = "{}/{}".format(login.API_URL,url_ext.SEARCH)
    client = ServerApi(api_url=API_URL)

    response = client.post_with_bearer_token(
                    {
                        "nric": resp['nric'],
                        "dateOfBirth": resp['dateofBirth'].split("T")[0]
                    }
                )
                
    assert response.status_code == 200
    assert response.json()['id'] == resp['id']
    assert response.json()['nric'] == resp['nric']
    assert response.json()['dateofBirth'] == resp['dateofBirth']
    assert response.json()['fullName'] == resp['fullName']
    assert response.json()['gender'] == resp['gender']

    return response.json()['id']

def create_flow():
    API_URL = "{}/{}".format(login.API_URL,url_ext.CREATE)
    client = ServerApi(api_url=API_URL)
    
    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    response = client.post_with_bearer_token(
                    create_patient_1a(details)
                )
    
    assert response.status_code == 200
    return response

def socialmed_create_flow(patient_id='', custom_dict={}):
    API_URL = "{}/{}".format(login.API_URL,url_ext.SOCIAL_MED_CREATE)
    client = ServerApi(api_url=API_URL)
    
    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    patient_1b = create_patient_1b(details,custom_dict,patient_id)

    response = client.post_with_bearer_token(
                    patient_1b
                )
    assert response.status_code == 200
    return response

def episode_listing_flow(patient_id=''):
    API_URL = "{}/{}".format(login.API_URL,url_ext.LISTING)
    client = ServerApi(api_url=API_URL)

    response = client.post_with_bearer_token(
                    {
                        "patientId": patient_id
                    }
                )
    
    assert response.status_code == 200
    return response

def social_med_flow(episode_id=''):
    API_URL = "{}/{}".format(login.API_URL,url_ext.SOCIAL_MED)
    client = ServerApi(api_url=API_URL)

    response = client.post_with_bearer_token(
                    {
                        "episodeId": episode_id
                    }
                )
    
    assert response.status_code == 200
    return response

def caresetting_active_flow(episode_id=''):
    API_URL = "{}/{}".format(login.API_URL,url_ext.CARESETTING_ACTIVE)
    client = ServerApi(api_url=API_URL)

    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    response = client.post_with_bearer_token(
                    {
                        "episodeId": episode_id,
                        "organizationCenter": details["orgCenterResponseCode"]
                    }
                )
    
    assert response.status_code == 200
    return response

def caresetting_create_flow(patient_id='', episode_id='', status='', custom_dict={}):
    API_URL = "{}/{}".format(login.API_URL,url_ext.CARESETTING_CREATE)
    client = ServerApi(api_url=API_URL)

    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    response = client.post_with_bearer_token(
                    create_caresetting(details, custom_dict, patient_id, episode_id, status)
                )
    
    assert response.status_code == 200
    return response

def coreoutcome_flow(caresetting_id=''):
    API_URL = "{}/{}".format(login.API_URL,url_ext.COREOUTCOME)
    client = ServerApi(api_url=API_URL)

    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    response = client.post_with_bearer_token(
                    {
                        "careSettingId": caresetting_id   
                    }
                )
    
    assert response.status_code == 200
    return response

def eq5d_flow(custom_dict={}, caresetting_date_assessed='', caresetting_id='', type='A', assessment_id=None, assessed_by=None, is_draft=True):
    if is_draft:
        API_URL = "{}/{}".format(login.API_URL,url_ext.EQ5D_DRAFT)
        status = 'Draft'
    else:
        API_URL = "{}/{}".format(login.API_URL,url_ext.EQ5D_CREATE)
        status = 'Submit'
    client = ServerApi(api_url=API_URL)

    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    response = client.post_with_bearer_token(
                    create_draft_eq5d(
                        details = details, 
                        custom_dict = custom_dict, 
                        caresetting_date_assessed = caresetting_date_assessed, 
                        caresetting_id = caresetting_id, 
                        status = status,
                        assessment_id = assessment_id,
                        type = type,
                        assessed_by = assessed_by
                    )
                )
    
    assert response.status_code == 200
    return response

def fim_flow(custom_dict={}, caresetting_date_assessed='', caresetting_id='', type='A', assessment_id=None, assessed_by=None, is_draft=True):
    if is_draft:
        API_URL = "{}/{}".format(login.API_URL,url_ext.FIM_DRAFT)
        status = 'Draft'
    else:
        API_URL = "{}/{}".format(login.API_URL,url_ext.FIM_CREATE)
        status = 'Submit'

    client = ServerApi(api_url=API_URL)

    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    response = client.post_with_bearer_token(
                    create_draft_fim(
                        details = details, 
                        custom_dict = custom_dict, 
                        caresetting_date_assessed = caresetting_date_assessed, 
                        caresetting_id = caresetting_id, 
                        status = status,
                        assessment_id = assessment_id,
                        type = type,
                        assessed_by = assessed_by
                    )
                )
    
    assert response.status_code == 200
    return response

def section_1_2_flow():
    # Create 1a
    response = create_flow()
    # Search
    patient_id = search_flow(response.json())
    # Create 1b
    response_section_1b = socialmed_create_flow(patient_id)
    # Episode listing
    response_episode_listing = episode_listing_flow(patient_id)
    # Social Med
    response_social_med = social_med_flow(response_episode_listing.json()['episodes'][0]['id'])
    # Care Setting Active
    response_caresetting_active = caresetting_active_flow(response_episode_listing.json()['episodes'][0]['id'])
    # Create Care Setting (Section 2)
    response_caresetting_create = caresetting_create_flow(
            patient_id=patient_id,
            episode_id=response_episode_listing.json()['episodes'][0]['id'],
            status=response_episode_listing.json()['episodes'][0]['status']
        )
    # Episode listing 2
    response_episode_listing_2 = episode_listing_flow(patient_id)
    # Core Outcome
    response_coreoutcome = coreoutcome_flow(response_caresetting_create.json()['id'])

    response_section_1b = response_section_1b.json()
    response_episode_listing = response_episode_listing.json()
    response_social_med = response_social_med.json()
    response_caresetting_create = response_caresetting_create.json()
    response_episode_listing_2 = response_episode_listing_2.json()
    response_coreoutcome = response_coreoutcome.json()

    return response_caresetting_create

def assessment_flow(assessment_category='EQ5D', assessment_id=""):
    API_URL = "{}/{}".format(login.API_URL,url_ext.ASSESSMENT)
    client = ServerApi(api_url=API_URL)

    details = get_details_after_login(login.EMAIL,login.DOMAIN)

    response = client.post_with_bearer_token(
                    {
                        "assessmentCategory": assessment_category,
                        "assessmentId": assessment_id
                    }
                )
    
    assert response.status_code == 200
    return response

def assert_eq5d(response_admission=[], response_assessment=[]):
    assert response_admission['assessmentId'] == response_assessment['questionAnswers'][0]['answer']
    assert response_admission['assessmentFormStatus'] == response_assessment['questionAnswers'][4]['answer']
    assert response_admission['assessedby'] == response_assessment['questionAnswers'][5]['answer']
    assert response_admission['mobility'] == response_assessment['questionAnswers'][6]['answer']
    assert response_admission['selfCare'] == response_assessment['questionAnswers'][7]['answer']
    assert response_admission['usualActivities'] == response_assessment['questionAnswers'][8]['answer']
    assert response_admission['painOrDiscomfort'] == response_assessment['questionAnswers'][9]['answer']
    assert response_admission['anxietyDepression'] == response_assessment['questionAnswers'][10]['answer']
    assert response_admission['rateHealth'] == response_assessment['questionAnswers'][11]['answer']
    assert "False" == response_assessment['questionAnswers'][14]['answer']
    assert response_admission['careSettingId'] == response_assessment['questionAnswers'][18]['answer']

def assert_fim(response_admission=[], response_assessment=[]):
    assert response_admission['assessmentId'] == response_assessment['questionAnswers'][0]['answer']
    assert response_admission['formVersion'] == response_assessment['questionAnswers'][1]['answer']
    assert response_admission['assessmentType'] == response_assessment['questionAnswers'][3]['answer']
    assert response_admission['assessmentFormStatus'] == response_assessment['questionAnswers'][4]['answer']
    assert response_admission['assessedby'] == response_assessment['questionAnswers'][5]['answer']
    assert response_admission['eating'] == response_assessment['questionAnswers'][6]['answer']
    assert response_admission['grooming'] == response_assessment['questionAnswers'][7]['answer']
    assert response_admission['bathing'] == response_assessment['questionAnswers'][8]['answer']
    assert response_admission['dressingUpper'] == response_assessment['questionAnswers'][9]['answer']
    assert response_admission['dressingLower'] == response_assessment['questionAnswers'][10]['answer']
    assert response_admission['toileting'] == response_assessment['questionAnswers'][11]['answer']
    assert response_admission['bladder'] == response_assessment['questionAnswers'][12]['answer']
    assert response_admission['bowel'] == response_assessment['questionAnswers'][13]['answer']
    assert response_admission['transfer'] == response_assessment['questionAnswers'][14]['answer']
    assert response_admission['transferToilet'] == response_assessment['questionAnswers'][15]['answer']
    assert response_admission['transferBath'] == response_assessment['questionAnswers'][16]['answer']
    assert response_admission['locomotionType'] == response_assessment['questionAnswers'][17]['answer']
    
    if response_admission['locomotionType'] == 'W':
        assert response_admission['locomotionWalk'] == response_assessment['questionAnswers'][18]['answer']
        assert "" == response_assessment['questionAnswers'][19]['answer']
        assert "" == response_assessment['questionAnswers'][20]['answer']
    elif response_admission['locomotionType'] == 'WH':
        assert "" == response_assessment['questionAnswers'][18]['answer']
        assert response_admission['locomotionWheelchair'] == response_assessment['questionAnswers'][19]['answer']
        assert "" == response_assessment['questionAnswers'][20]['answer']
    elif response_admission['locomotionType'] == 'B':
        assert "" == response_assessment['questionAnswers'][18]['answer']
        assert "" == response_assessment['questionAnswers'][19]['answer']
        assert response_admission['locomotionBoth'] == response_assessment['questionAnswers'][20]['answer']
    assert response_admission['stairs'] == response_assessment['questionAnswers'][21]['answer']
    assert str(response_admission['motorSubScore']) == response_assessment['questionAnswers'][22]['answer']
    assert response_admission['comprehension'] == response_assessment['questionAnswers'][23]['answer']
    assert response_admission['comprehensionCategory'] == response_assessment['questionAnswers'][24]['answer']
    assert response_admission['expression'] == response_assessment['questionAnswers'][25]['answer']
    assert response_admission['expressionCategory'] == response_assessment['questionAnswers'][26]['answer']
    assert response_admission['socialInteraction'] == response_assessment['questionAnswers'][27]['answer']
    assert response_admission['problemSolving'] == response_assessment['questionAnswers'][28]['answer']
    assert response_admission['memory'] == response_assessment['questionAnswers'][29]['answer']
    assert str(response_admission['cognitiveSubScore']) == response_assessment['questionAnswers'][30]['answer']
    assert str(response_admission['totalScore']) == response_assessment['questionAnswers'][31]['answer']
    assert 'False' == response_assessment['questionAnswers'][34]['answer']
    assert response_admission['careSettingId'] == response_assessment['questionAnswers'][38]['answer']
    assert response_admission['id'] == response_assessment['questionAnswers'][39]['answer']

# create_draft_eq5d(details={}, custom_dict={}, caresetting_date_assessed = '', caresetting_id='', status='Draft', type='A')




# def update_discharged_list(total_records=None, current_page_number=None, \
#                         total_page=None, items=[]):
#     local.DISCHARGED_LIST_TOTAL_RECORDS = total_records
#     local.DISCHARGED_LIST_TOTAL_PAGE = total_page
#     local.DISCHARGED_LIST_ITEMS = items

#     return local.DISCHARGED_LIST_ITEMS

# def text_to_json(text):
#     return json.dumps(text)


# def compose_response_msg(response: Response):
#     req = response.request
#     req_body = ''
#     if isinstance(req.body, str):
#         req_body = req.body
#     elif isinstance(req.body, bytearray) or isinstance(req.body, bytes):
#         req_body = req.body.decode(encoding='utf8')

#     request_id = req.headers.get('X-Request-Id', '')

#     return 'Request(id: {request_id}) \n  {method} {url} {req_body} RETURNS \n  Response [{status}] {resp_body}' \
#         .format(request_id=request_id,
#                 method=req.method,
#                 url=response.url,
#                 req_body=req_body,
#                 status=response.status_code,
#                 resp_body=response.text)


# def json_schema_check(response, schema, expected_status=200, resolver=None):
#     assert response.status_code == expected_status, \
#         'Failed to check status code, expected: {}. {}'.format(expected_status, compose_response_msg(response))
#     try:
#         json_response = response.json()
#     except ValueError or JSONDecodeError:
#         json_response = None
#     if schema is None:
#         assert json_response is None or json_response == "", \
#             'A None schema should match with a None response. {}'.format(compose_response_msg(response))
#     elif len(schema) == 0:
#         assert json_response is not None and len(json_response) == 0, \
#             'An empty schema should match with an empty response. {}'.format(compose_response_msg(response))
#     else:
#         try:
#             validate(json_response, schema, resolver=resolver)
#         except Exception as error:
#             assert not isinstance(error, SchemaError), \
#                 'Schema is invalid. Please check it.\n{}'.format(error)
#             assert not isinstance(error, ValidationError), \
#                 'Schema check failed. {}\n{}'.format(compose_response_msg(response), error)
#             raise error


# def generate_random_string(length):
#     letters = string.ascii_lowercase
#     result_str = ''.join(random.choice(letters) for _ in range(length))
#     return result_str


# def generate_random_date():
#     day = random.randint(1, 30)
#     if day < 10:
#         day = '0{}'.format(day)
#     else:
#         day = str(day)
#     month = random.randint(1, 12)
#     if month < 10:
#         month = '0{}'.format(month)
#     else:
#         month = str(month)
#     year = str(random.randint(2020, 2030))
#     return '{}-{}-{}'.format(year, month, day)

