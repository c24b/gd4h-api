from datetime import datetime
from venv import create
import requests
import json 
from pymongo import MongoClient
from bson import ObjectId

DATABASE_NAME = "GD4H_V2"
mongodb_client = MongoClient("mongodb://localhost:27017")
DB = mongodb_client[DATABASE_NAME]
TEST_URL = "http://api.gd4h.fr/"
def get_datasets():
    r = requests.get(TEST_URL+"datasets")
    assert r.status_code == 200, r.status_code
    datasets = r.json()
    values = datasets[0].keys()
    assert sorted(values) ==sorted(['state', 'organizations', 'data_domain', 'theme_category', 'qualification_comments', 'nature', 'environment', 'subthematic', 'exposure_factor_category', 'name', 'acronym', 'description', 'has_filter', 'has_search_engine', 'integration_status', 'is_opendata', 'license_name', 'license_type', 'has_restrictions', 'restrictions_comments', 'downloadable', 'broadcast_mode', 'is_geospatial_data', 'geographical_geospatial_coverage', 'geographical_information_level', 'projection_system', 'related_geographical_information', 'has_related_referential', 'year_start', 'year_end', 'year', 'temporal_scale', 'update_frequency', 'automatic_update', 'last_updated', 'format', 'data_format', 'metrics_registered_elements', 'volume', 'measurement_data', 'has_documentation', 'documentation_comments', 'has_missing_data', 'missing_data_comments', 'has_compliance', 'compliance_comments', 'has_pricing', 'pricing_comments', 'contact_type_comments', 'last_inserted', 'last_modification', 'comments', 'related_datasets', 'other_access_points', 'url', '_id'])
    assert len(datasets) == 114

def get_datasets_en():
    r = requests.get(TEST_URL+"datasets/?lang=en")
    assert r.status_code == 200, r.status_code
    datasets = r.json()
    assert datasets[0]["update_frequency"] == ["Irregular"]
    
    assert sorted(datasets[110].keys()) ==sorted(['state', 'organizations', 'data_domain', 'theme_category', 'qualification_comments', 'nature', 'environment', 'subthematic', 'exposure_factor_category', 'name', 'acronym', 'description', 'has_filter', 'has_search_engine', 'integration_status', 'is_opendata', 'license_name', 'license_type', 'has_restrictions', 'restrictions_comments', 'downloadable', 'broadcast_mode', 'is_geospatial_data', 'geographical_geospatial_coverage', 'geographical_information_level', 'projection_system', 'related_geographical_information', 'has_related_referential', 'year_start', 'year_end', 'year', 'temporal_scale', 'update_frequency', 'automatic_update', 'last_updated', 'format', 'data_format', 'metrics_registered_elements', 'volume', 'measurement_data', 'has_documentation', 'documentation_comments', 'has_missing_data', 'missing_data_comments', 'has_compliance', 'compliance_comments', 'has_pricing', 'pricing_comments', 'contact_type_comments', 'last_inserted', 'last_modification', 'comments', 'related_datasets', 'other_access_points', 'url', '_id'])
    assert len(datasets) ==114

def get_dataset():
    r = requests.get(TEST_URL+"datasets/61fdb1c4c917bd760bc3f99a")
    assert r.status_code == 200, r.status_code
    dataset = r.json()
    assert dataset["name"] == "Adresses"
    assert sorted(list(dataset.keys())) == sorted(['state', 'organizations', 'data_domain', 'theme_category', 'qualification_comments', 'nature', 'environment', 'subthematic', 'exposure_factor_category', 'name', 'acronym', 'description', 'has_filter', 'has_search_engine', 'integration_status', 'is_opendata', 'license_name', 'license_type', 'has_restrictions', 'restrictions_comments', 'downloadable', 'broadcast_mode', 'is_geospatial_data', 'geographical_geospatial_coverage', 'geographical_information_level', 'projection_system', 'related_geographical_information', 'has_related_referential', 'year_start', 'year_end', 'year', 'temporal_scale', 'update_frequency', 'automatic_update', 'last_updated', 'format', 'data_format', 'metrics_registered_elements', 'volume', 'measurement_data', 'has_documentation', 'documentation_comments', 'has_missing_data', 'missing_data_comments', 'has_compliance', 'compliance_comments', 'has_pricing', 'pricing_comments', 'contact_type_comments', 'last_inserted', 'last_modification', 'comments', 'related_datasets', 'other_access_points', 'url', '_id'])

def get_dataset_en():
    r = requests.get(TEST_URL+"datasets/61fdb1c4c917bd760bc3f99a/?lang=en")
    assert r.status_code == 200
    dataset = r.json()
    
    assert dataset["name"] == "Adresses"
    assert sorted(list(dataset.keys())) == sorted(['state', 'organizations', 'data_domain', 'theme_category', 'qualification_comments', 'nature', 'environment', 'subthematic', 'exposure_factor_category', 'name', 'acronym', 'description', 'has_filter', 'has_search_engine', 'integration_status', 'is_opendata', 'license_name', 'license_type', 'has_restrictions', 'restrictions_comments', 'downloadable', 'broadcast_mode', 'is_geospatial_data', 'geographical_geospatial_coverage', 'geographical_information_level', 'projection_system', 'related_geographical_information', 'has_related_referential', 'year_start', 'year_end', 'year', 'temporal_scale', 'update_frequency', 'automatic_update', 'last_updated', 'format', 'data_format', 'metrics_registered_elements', 'volume', 'measurement_data', 'has_documentation', 'documentation_comments', 'has_missing_data', 'missing_data_comments', 'has_compliance', 'compliance_comments', 'has_pricing', 'pricing_comments', 'contact_type_comments', 'last_inserted', 'last_modification', 'comments', 'related_datasets', 'other_access_points', 'url', '_id'])

def get_organizations():
    r = requests.get(TEST_URL+"organizations")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 43
    
def get_organizations_en():
    r = requests.get(TEST_URL+"organizations/?lang=en")
    assert r.status_code == 200, r.status_code
    items = r.json()
    assert len(items) == 43
    assert items[0]['organization_type'] == 'Association law 1901', items[0]['organization_type']

def get_organization():
    r = requests.get(TEST_URL+"organizations/61fdb1c2c917bd760bc3f96f")
    assert r.status_code == 200, r.status_code
    item = r.json()
    assert item["url"] == 'http://www.acoucité.org'
    assert item['organization_type'] == 'Association loi 1901'

def get_organization_en():
    r = requests.get(TEST_URL+"organizations/61fdb1c2c917bd760bc3f96f/?lang=en")
    assert r.status_code == 200
    item = r.json()
    assert item["url"] == 'http://www.acoucité.org'
    assert item['organization_type'] == 'Association law 1901', item['organization_type']

def get_organization_filters():
    r = requests.get(TEST_URL+"organizations/filters/")
    assert r.status_code == 200, r.status_code
    filters = r.json()
    assert sorted(["name", 'is_controled', "is_multiple", 'is_bool', 'values']) == sorted(filters[0].keys()), filters[0].keys() 
        
def get_dataset_filters():
    r = requests.get(TEST_URL+"datasets/filters/")
    assert r.status_code == 200, r.status_code
    filters = r.json()
    assert filters[0]["values"][0] == "Agence publique", repr(filters[0]["values"][0])
    assert sorted(["name", 'is_controled', "is_multiple", 'is_bool', 'values']) == sorted(filters[0].keys()), filters[0].keys()

def get_dataset_filters_en():
    r = requests.get(TEST_URL+"datasets/filters/?lang=en")
    assert r.status_code == 200, r.status_code
    filters = r.json()
    assert sorted(["name", 'is_controled', "is_multiple", 'is_bool', 'values']) == sorted(filters[0].keys()), filters[0].keys()
    assert filters[0]["values"][0] == "Administrative Public Institution", filters[0]["values"][0] 
def search_dataset_001():
    r = requests.get(TEST_URL+"datasets/search?query=m%C3%A9taux%20lourds&lang=fr")
    assert r.status_code == 200, r.status_code
    response = r.json()
    assert "count" in response
    assert "results" in response
    assert "query" in response
    assert response["query"] == "métaux lourds", response["query"]
    assert response["results"][1]['geographical_information_level'] == ['Station de mesure'], response["results"][1]

def search_dataset_002():
    r = requests.get(TEST_URL+"datasets/search?query=bruit%20Grenoble&lang=fr")
    assert r.status_code == 200, r.status_code
    response = r.json()
    assert "count" in response
    assert "results" in response
    assert "query" in response
    assert response["query"] == "bruit Grenoble", response["query"]
    assert response["results"][0]["description"] == "", response["results"][0]["description"]
    assert response["results"][0]["name"] == "Mesures de bruit dans l'agglomération de Grenoble", response["results"][0]["name"]
    
def filter_dataset_001():
    data = {"organizations": ["ANSES", "BRGM"]}
    r = requests.post(TEST_URL+"datasets/filters",data=json.dumps(data))
    assert r.status_code == 200, r.status_code
    response = r.json()
    assert response["count"] == 10, response

def filter_dataset_002():
    data = {
        "is_opendata": True,
        "downloadable": True,
        "is_geospatial_data": True
    }
    r = requests.post(TEST_URL+"datasets/filter/", data=json.dumps(data))
    assert r.status_code == 200, r.status_code
    assert r.json()["count"] == 47

def filter_dataset_003():
    data = {
        "environment": ["Air", "Eau"],
    }
    r = requests.post(TEST_URL+"datasets/filter/", data=json.dumps(data))
    assert r.status_code == 200, r.status_code
    assert r.json()["results"][0]['name'] == "Banque nationale d'Accès aux Données sur les Eaux Souterraines"
    assert r.json()["count"] == 47

def filter_dataset_004():
    data = {
        "environment": ["Pollution", "Eau"],
    }
    r = requests.post(TEST_URL+"datasets/filter/", data=json.dumps(data))
    assert r.status_code == 422, r.status_code
    assert r.json()['detail'][0]['msg']== "value is not a valid enumeration member; permitted: 'Air', 'Eau', 'Sols', 'Alimentation'"

def filter_dataset_005():
    data = {
        "is_opendata": True,
        "environment": ["Air", "Eau"],
        "organizations": ["ANSES"]
    }
    r = requests.post(TEST_URL+"datasets/filter/", data=json.dumps(data))
    assert r.status_code == 404, r.status_code

def filter_dataset_006():
    data = {
        "is_opendata": True,
        "organizations": ["ANSES"]
    }
    r = requests.post(TEST_URL+"datasets/filter/", data=json.dumps(data))
    assert r.status_code == 200, r.status_code
    assert r.json()["count"] == 1, r.json()["count"]
    assert r.json()["results"][0]["name"] == "Etude de l'Alimentation Totale 2 (EAT)", r.json()["results"][0]["name"]

def get_comment():
    r = requests.get(TEST_URL+"comments/")
    assert r.status_code == 200, r.status_code
    assert r.json()[0] == {'_id': {'$oid': '61fdddb2b3593e619f4ffd5b'}, 'text': 'Sols', 'user': 'admin', 'date': {'$date': 1644030914925}, 'perimeter': 'dataset', 'scope': 'qualification_comments', 'ref_id': {'$oid': '61fdb1c4c917bd760bc3f99a'}, 'lang': 'fr'}

def add_general_comment():
    print("General_comment")
    example_comment = {
        "text": "Ceci est un commentaire de test général sur la plateforme", "user": "admin"}
    r = requests.post(TEST_URL+"comments/", data=json.dumps(example_comment))
    assert r.status_code == 201, r.status_code
    print(r.json()[0])
    created_comment = DB.comments.find_one(example_comment)
    assert created_comment["user"] == "admin"
    assert created_comment["text"] == example_comment["text"]
    DB.comments.delete_one(example_comment)
    # DB.comments.delete({"_id": created_comment_id})   

def add_general_dataset_comment():
    dataset = DB.datasets.find_one()
    dataset_id = str(dataset["_id"])
    example_comment = {
        "text": f"Ceci est un commentaire de test général sur le dataset #{dataset_id}", 
        "user": "admin",
        "scope": "dataset",
        "field": "comments",
        "ref_id": dataset_id
    }
    r = requests.post(TEST_URL+"comments/", data=json.dumps(example_comment))
    assert r.status_code == 201, r.status_code
    created_comment = DB.comments.find_one(example_comment)
    assert created_comment["user"] == "admin"
    assert created_comment["text"] == example_comment["text"]
    assert dataset["comments"][-1]["text"] == example_comment["text"]
    DB.comments.delete_one(example_comment)
    DB.datasets.update_one( { "_id": dataset_id }, { "$pop": {"comments": -1 } } )

def add_technical_comment():
    dataset = DB.datasets.find_one()
    dataset_id = str(dataset["_id"])
    example_comment = {
        "text": f"Ceci est un commentaire de test sur le  dataset #{dataset_id} dans le champ: context_comments", 
        "user": "admin",
        "scope": "dataset",
        "field": "context_comments",
        "ref_id": dataset_id
    }
    r = requests.post(TEST_URL+"comments/", data=json.dumps(example_comment))
    assert r.status_code == 201, r.status_code
    created_comment = DB.comments.find_one(example_comment)
    assert created_comment["user"] == "admin"
    assert created_comment["text"] == example_comment["text"]
    assert dataset["context_comments"][-1]["text"] == example_comment["text"]
    DB.comments.delete_one(example_comment)
    DB.datasets.update_one( { "_id": dataset_id }, { "$pop": {"context_comments": -1 } } )
    
if __name__ == "__main__":
    get_datasets()
    # get_datasets_en()
    # get_dataset()
    # get_dataset_en()
    get_organizations()
    get_organizations_en()
    # get_organization()
    # get_organization_en()
    # get_organization_filters()
    # get_dataset_filters()
    # get_dataset_filters_en()
    search_dataset_001()
    search_dataset_002()
    filter_dataset_001()
    filter_dataset_002()
    filter_dataset_003()
    filter_dataset_004()
    filter_dataset_005()
    filter_dataset_006()
    get_comment()
    add_general_comment()
    add_general_dataset_comment()
    add_technical_comment()