    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        print(body)
        newstation = {
            "Latitude": body["Lat"],
            "Longitude": body["Long"],
            "State": body["State"],
            "IsNewStation": body["IsNew"],
            "StationCode": body["Code"],
            "StationName": body["Name"],

        }
        x = collection1.insert_one(newstation)
        newstation["_id"] = str(x.inserted_id)  # Convert ObjectId to string
        response_data = {
            "status": "success",
            "message": "New station added successfully",
            "data": newstation,
        }
