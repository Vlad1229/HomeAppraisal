from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from Services.DwellingService import DwellingService
from Services.RegionService import RegionService
from Services.UserService import UserService

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

user_service = UserService()
region_service = RegionService()
dwelling_service = DwellingService()

@app.route("/register_user", methods=["POST"])
@cross_origin()
def register_user():
    if request.method == 'POST':
        user_id = request.form.get("nickname")
        email = request.form.get("email")
        password = request.form.get("password")

        response = jsonify({'success': user_service.add_user(user_id, email, password, True)})
        return response

    else:
        return jsonify({'success': False})


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    if request.method == 'POST':
        nickname = request.form.get("nickname")
        password = request.form.get("password")

        result = user_service.auth_user(nickname, password)
        if result["token"] is not None:
            response = jsonify({"success": True, "result": result})
            return response
        else:
            return jsonify({'success': False})

    else:
        return jsonify({'success': False})


@app.route("/verify", methods=["POST"])
@cross_origin()
def verify():
    if request.method == 'POST':
        token = request.form.get("token")

        response = user_service.user_is_admin(token)
        return {'response': response}

    else:
        return {'response': False}


@app.route("/add_region", methods=["POST"])
@cross_origin()
def add_region():
    if request.method == 'POST':
        region_data = {}
        region_data["region_name"] = request.form.get("region_name")
        region_data["crime_rate"] = request.form.get("crime_rate")
        region_data["river"] = request.form.get("river")
        region_data["nitric_oxides"] = request.form.get("nitric_oxides")
        region_data["rooms_average_num"] = request.form.get("rooms_average_num")
        region_data["tax_rate"] = request.form.get("tax_rate")
        region_data["pupil_teacher_ratio"] = request.form.get("pupil_teacher_ratio")
        region_data["lower_status_percentage"] = request.form.get("lower_status_percentage")
        region_data["region_coefficient"] = 0.811

        response = jsonify({'success': region_service.add_region(region_data)})
        return response

    else:
        return {'response': False}


@app.route("/update_region", methods=["PUT"])
@cross_origin()
def update_region():
    if request.method == 'PUT':
        global region_index
        region_data = {}
        region_data["id"] = request.form.get("id")
        region_data["region_name"] = request.form.get("region_name")
        region_data["crime_rate"] = request.form.get("crime_rate")
        region_data["river"] = request.form.get("river")
        region_data["nitric_oxides"] = request.form.get("nitric_oxides")
        region_data["rooms_average_num"] = request.form.get("rooms_average_num")
        region_data["tax_rate"] = request.form.get("tax_rate")
        region_data["pupil_teacher_ratio"] = request.form.get("pupil_teacher_ratio")
        region_data["lower_status_percentage"] = request.form.get("lower_status_percentage")
        region_data["region_coefficient"] = 0.911
        response = jsonify({'success': region_service.update_region(region_data)})

        dwellings = dwelling_service.get_dwellings_in_region(region_data["id"])
        for dwelling in dwellings:
            dwelling_data = {}
            dwelling_data["id"] = dwelling[0]
            dwelling_data["address"] = dwelling[1]
            dwelling_data["user_id"] = dwelling[2]
            dwelling_data["region_id"] = dwelling[3]
            dwelling_data["rooms_num"] = dwelling[4]
            dwelling_data["size"] = dwelling[5]
            dwelling_data["floor"] = dwelling[6]
            dwelling_data["floors_total"] = dwelling[7]
            dwelling_data["walls"] = dwelling[8]
            dwelling_data["repair"] = dwelling[9]
            dwelling_data["planning"] = dwelling[10]
            dwelling_data["furniture"] = dwelling[11]
            dwelling_data["type"] = dwelling[12]
            dwelling_data["sale_term"] = dwelling[13]
            dwelling_data["cost"] = dwelling[14]
            dwelling_data["is_relevant"] = False
            dwelling_service.update_dwelling(dwelling_data)

        response = jsonify({'success': region_service.update_region(region_data)})
        return response

    else:
        return {'response': False}


@app.route("/delete_region", methods=["DELETE"])
@cross_origin()
def delete_region():
    if request.method == 'DELETE':
        response = jsonify({'success': region_service.delete_region(request.form.get("id"))})
        return response

    else:
        return {'response': False}


@app.route("/get_regions", methods=["GET"])
@cross_origin()
def get_regions():
    if request.method == 'GET':
        response = jsonify({"success": True, "result": region_service.get_regions()})
        return response

    else:
        return {'response': False}


@app.route("/get_region", methods=["GET"])
@cross_origin()
def get_region():
    if request.method == 'GET':
        region = region_service.get_region(request.args.get('id'))
        response = jsonify({"success": region is not None, "result": region})
        return response

    else:
        return {'response': False}


@app.route("/add_dwelling", methods=["POST"])
@cross_origin()
def add_dwelling():
    if request.method == 'POST':
        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return {'response': False}, 401

        token = authorization_header.replace("Bearer ", "")

        dwelling_data = {}
        dwelling_data["user_id"] = UserService.get_user_id(token)
        dwelling_data["address"] = request.form.get("address")
        dwelling_data["region_id"] = request.form.get("region_id")
        dwelling_data["rooms_num"] = request.form.get("rooms_num")
        dwelling_data["size"] = request.form.get("size")
        dwelling_data["floor"] = request.form.get("floor")
        dwelling_data["floors_total"] = request.form.get("floors_total")
        dwelling_data["walls"] = request.form.get("walls")
        dwelling_data["repair"] = request.form.get("repair")
        dwelling_data["planning"] = request.form.get("planning")
        dwelling_data["furniture"] = request.form.get("furniture")
        dwelling_data["type"] = request.form.get("type")
        dwelling_data["sale_term"] = request.form.get("sale_term")
        dwelling_data["cost"] = 80000
        dwelling_data["is_relevant"] = True

        response = jsonify({'success': dwelling_service.add_dwelling(dwelling_data)})
        return response

    else:
        return {'response': False}


@app.route("/update_dwelling", methods=["PUT"])
@cross_origin()
def update_dwelling():
    if request.method == 'PUT':
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.replace("Bearer ", "")
        if token == "":
            return {'response': False}, 401

        dwelling_data = {}
        dwelling_data["id"] = request.form.get("id")
        dwelling_data["address"] = request.form.get("address")
        dwelling_data["user_id"] = UserService.get_user_id(token)
        dwelling_data["region_id"] = request.form.get("region_id")
        dwelling_data["rooms_num"] = request.form.get("rooms_num")
        dwelling_data["size"] = request.form.get("size")
        dwelling_data["floor"] = request.form.get("floor")
        dwelling_data["floors_total"] = request.form.get("floors_total")
        dwelling_data["walls"] = request.form.get("walls")
        dwelling_data["repair"] = request.form.get("repair")
        dwelling_data["planning"] = request.form.get("planning")
        dwelling_data["furniture"] = request.form.get("furniture")
        dwelling_data["type"] = request.form.get("type")
        dwelling_data["sale_term"] = request.form.get("sale_term")
        dwelling_data["cost"] = 90000
        dwelling_data["is_relevant"] = True

        response = jsonify({'success': dwelling_service.update_dwelling(dwelling_data)})
        return response

    else:
        return {'response': False}

@app.route("/recalculate_dwelling", methods=["PUT"])
@cross_origin()
def recalculate_dwelling():
    global dwelling_index
    if request.method == 'PUT':
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.replace("Bearer ", "")
        if token == "":
            return {'response': False}, 401

        response = jsonify({'success': dwelling_service.update_dwelling_cost(request.form.get("id"), 70000)})
        return response

    else:
        return {'response': False}

@app.route("/delete_dwelling", methods=["DELETE"])
@cross_origin()
def delete_dwelling():
    if request.method == 'DELETE':
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.replace("Bearer ", "")
        if token == "":
            return {'response': False}, 401

        response = jsonify({'success': dwelling_service.delete_dwelling(request.form.get("id"))})
        return response

    else:
        return {'response': False}


@app.route("/get_dwellings", methods=["GET"])
@cross_origin()
def get_dwellings():
    if request.method == 'GET':
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.replace("Bearer ", "")
        if token == "":
            return {'response': False}, 401

        response = jsonify({"success": True, "result": dwelling_service.get_dwellings(UserService.get_user_id(token))})
        return response

    else:
        return {'response': False}


@app.route("/get_dwelling", methods=["GET"])
@cross_origin()
def get_dwelling():
    if request.method == 'GET':
        authorization_header = request.headers.get('Authorization')
        token = authorization_header.replace("Bearer ", "")
        if token == "":
            return {'response': False}, 401

        token = authorization_header.replace("Bearer ", "")

        dwelling = dwelling_service.get_dwelling(request.args.get('id'))
        response = jsonify({"success": dwelling is not None, "result": dwelling})
        return response

    else:
        return {'response': False}


if __name__ == "__main__":
    app.run(debug=True)