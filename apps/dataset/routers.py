#!/usr/bin/.env/python3.9
# file: routers.py

import json
from bson.objectid import ObjectId
from fastapi import APIRouter, Body, Request, HTTPException, status,Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from bson import json_util, ObjectId

from .models import Dataset
from .models import FilterDatasetFr, FilterDatasetEn
from typing import Optional
from .services import es, index_document, get_indexed_fieldnames, search_documents
from .services import sync_get_filters    
router = APIRouter()

def parse_json(data):
    return json.loads(json_util.dumps(data))

@router.get("/", response_description="Get all datasets")
async def get_datasets(request: Request, lang:str = "fr"):
    datasets = []
    for doc in await request.app.mongodb["datasets"].find({}).to_list(length=120):
        doc_id = doc["_id"]
        doc = doc[lang]
        doc["_id"] = str(doc_id)
        datasets.append(doc)
    if len(datasets) == 0:
        raise HTTPException(status_code=404, detail=f"No Datasets found")
    return parse_json(datasets)

@router.post("?lang=fr", response_description="Add a dataset")
async def create_dataset(request:Request, dataset: Dataset = Body(...), lang:str="fr"):
    dataset = parse_json(dataset)
    stored_dataset = {"en":{}, "fr":{}}
    stored_dataset[lang] = dataset
    #here translate
    #other_lang = SWITCH_LANGS(lang)
    #org[other_lang] = translate_doc(organization, _from=lang)
    #here index
    new_dataset = await request.app.mongodb["datasets"].insert_one(stored_dataset)
    created_dataset = await request.app.mongodb["datasets"].find_one({"_id": new_dataset.inserted_id})
    #here index document at insert
    index_document("dataset", create_dataset)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_dataset)

@router.put("/{item_id}", response_description="Update a dataset")
async def update_dataset(request:Request, item_id: str, dataset: Dataset = Body(...), lang:str="fr"):
    dataset = parse_json(dataset)
    stored_dataset = {"en":{}, "fr":{}}
    stored_dataset[lang] = dataset
    #here translate
    #other_lang = SWITCH_LANGS(lang)
    #org[other_lang] = translate_doc(organization, _from=lang)
    #here index
    # update_dataset= {lang: dataset}
    # new_dataset = await request.app.mongodb["datasets"].update_one({"_id": ObjectId(item_id), {"$set":{lang:dataset}})
    # created_dataset = await request.app.mongodb["datasets"].find_one({"_id": new_dataset.inserted_id})
    # #here index document at insert
    # index_document("dataset", create_dataset)
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_dataset)
    raise NotImplemented

@router.get("/search", response_description="Search for datasets using full_text_query")
async def search_datasets(request:Request, query: Optional[str] = Query(None, min_length=2, max_length=50), lang:str="fr"):
    fields = get_indexed_fieldnames(model="dataset")
    final_query = {
        "multi_match" : {
        "query":    query.strip(), 
        "fields": fields
        }
    }
    highlight = {
        
        "pre_tags" : "<em class='tag-fr highlight'>",
        "post_tags" :"</em>",
        "fields" : {f:{} for f in fields }
        }
    results = search_documents(final_query, highlight, model="dataset", lang=lang)
    results["query"] = query
    return results

@router.get("/filters")
async def get_filters(request:Request, lang: str="fr"):
    filters = sync_get_filters(lang)
    return parse_json(filters)


@router.post("/filters?lang=fr")
async def filter_datasets_fr(request:Request, filter:FilterDatasetFr, lang:str="fr"):
    req_filter = await request.json()
    index_name = f"datasets_{lang}"
    print(req_filter)
    if len(req_filter) == 1:
        param_k = list(req_filter.keys())[0]
        param_v = list(req_filter.values())[0]
        if param_k == "organizations":
            final_q = {
                "nested": {
                    "path": param_k,
                    "query": {
                    "match": {
                        f"{param_k}.name": ",".join(param_v)
                       }
                    }
                }
            }
            
        else:
            if isinstance(param_v, list):
                final_q = {"match": {param_k: {"query": ",".join(param_v)}}}
            else:
                final_q = {"match": {param_k: {"query": param_v}}}
        # highlight = {}
        # results = search_documents(final_q, highlight,model="dataset", lang=lang)
        print(final_q)
    else:
        must = []
        for key, val in req_filter.items():
            if key == "organizations":
                nested_q = {"nested": {
                    "path": key,
                    "query": {
                    "match": {
                        f"{key}.name": ",".join(val)
                       }
                    }
                }}
                must.append(nested_q)
            else:
                if isinstance(val, list):
                    must.append({"match":{key:",".join(val)}})
                else:
                    must.append({"match":{key:val}})
        final_q = {"bool" : { "must":must}}
        print(final_q)
    highlight = {}
    results = search_documents(final_q, highlight, model="dataset", lang=lang)
    results["query"] = req_filter
    print(results)
    return results

@router.post("/filters?lang=en")
async def filter_datasets_en(request:Request, filter:FilterDatasetEn, lang:str="en"):
    req_filter = await request.json()
    index_name = f"datasets_{lang}"
    print(index_name)
    print(req_filter)
    if len(req_filter) == 1:
        param_k = list(req_filter.keys())[0]
        param_v = list(req_filter.values())[0]
        if param_k == "organizations":
            final_q = {
                "nested": {
                    "path": param_k,
                    "query": {
                    "match": {
                        f"{param_k}.name": ",".join(param_v)
                       }
                    }
                }
            }
            
        else:
            if isinstance(param_v, list):
                final_q = {"match": {param_k: {"query": ",".join(param_v)}}}
            else:
                final_q = {"match": {param_k: {"query": param_v}}}
        # highlight = {}
        # results = search_documents(final_q, highlight,model="dataset", lang=lang)
        print(final_q)
    else:
        must = []
        for key, val in req_filter.items():
            if key == "organizations":
                nested_q = {"nested": {
                    "path": key,
                    "query": {
                    "match": {
                        f"{key}.name": ",".join(val)
                       }
                    }
                }}
                must.append(nested_q)
            else:
                if isinstance(val, list):
                    must.append({"match":{key:",".join(val)}})
                else:
                    must.append({"match":{key:val}})
        final_q = {"bool" : { "must":must}}
        print(final_q)
    highlight = {}
    results = search_documents(final_q, highlight, model="dataset", lang=lang)
    results["query"] = req_filter
    print(results)
    return results

@router.get("/{item_id}", response_description="Get one dataset")
async def get_dataset(request: Request, item_id: str, lang:str = "fr"):
    if (dataset := await request.app.mongodb["datasets"].find_one({"_id": ObjectId(item_id)})) is not None:
        doc_id = dataset["_id"]
        doc = dataset[lang]
        doc["_id"] = str(doc_id)
        return parse_json(doc)
        # return jsonable_encoder(doc)
    raise HTTPException(status_code=404, detail=f"Dataset {item_id} not found")

