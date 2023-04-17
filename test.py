from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://admin2:poolcool@cluster1.syijvpg.mongodb.net/?retryWrites=true&w=majority")

dbname = client["eduClimateAnalysis"]

collection = dbname["climateData"]

