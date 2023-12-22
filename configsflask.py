from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import re
import json
import mysql.connector 
from datetime import datetime as dt

mydb= mysql.connector.connect(
  host="localhost",
  user="example",
  password="Password123.",
  database="config_info"
)

mycursor=mydb.cursor()

mycursor.execute('''CREATE TABLE IF NOT EXISTS apt_configs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    package_name VARCHAR(255),
    distribution VARCHAR(255),
    status VARCHAR(255),
    version VARCHAR(255),
    architecture VARCHAR(255),
    installation_info VARCHAR(255),
    date VARCHAR(100)
)''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS snap_configs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    version VARCHAR(255),
    rev INT,
    tracking VARCHAR(255),
    publisher VARCHAR(255),
    notes TEXT,
    date VARCHAR(100)
)''')

mycursor.execute('''CREATE TABLE IF NOT EXISTS java_configs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(255),
    date_installed VARCHAR(255),
    server_VM_size VARCHAR(255),
    runtime_env_build TEXT,
    VM_build TEXT,
    date VARCHAR(100)                
                 
)''')


insert_stmt1=("INSERT INTO apt_configs(package_name,distribution,status,version,architecture,installation_info,date)"
            "VALUES (%s,%s,%s,%s,%s,%s,%s)"
            )

insert_stmt2=("INSERT INTO snap_configs(name,version,rev,tracking,publisher,notes,date)"
            "VALUES (%s,%s,%s,%s,%s,%s,%s)"
            )

insert_stmt3=("INSERT INTO java_configs(version,date_installed,server_VM_size,runtime_env_build,VM_build,date)"
            "VALUES (%s,%s,%s,%s,%s,%s)"
            )



app = Flask(__name__)
CORS(app)

@app.route("/get-apt-configs")
def get_apt_configs():
    try:
        apt_installed_output = subprocess.check_output(["apt", "list", "--installed"]).decode("utf-8")

        split_app = apt_installed_output.split('\n')
        split_app = split_app[1:-1]

        package_info_list = []

        for line in split_app:
            components = re.split(r'[\/\s]+', re.sub(r',(?=now)', ' ', line))
            if len(components) == 7 or len(components) == 8:
                components[-3] = ' '.join(components[-3:])
                del components[-2:]

            if len(components) == 5:
                components.insert(1, "null")

            package_info_dict = {
                'package_name': components[0],
                'distribution': components[1],
                'status': components[2],
                'version': components[3],
                'architecture': components[4],
                'installation_info': components[5],
                'date': dt.now().isoformat() 
            }

            package_info_list.append(package_info_dict)
            mycursor.execute(insert_stmt1, tuple(package_info_dict.values()))
            mydb.commit()



        return jsonify(package_info_list)

    except subprocess.CalledProcessError as e:
        return str(e), 500

@app.route("/get-snap-configs")
def get_snap_configs():
    try:
        snap_installed_output = subprocess.check_output(["snap", "list"]).decode("utf-8")

        lines = [line for line in snap_installed_output.strip().split('\n') if line.strip()]
        keys = lines[0].split()
        snap_info_list = []

        for line in lines[1:]:
            components = line.split(maxsplit=len(keys) - 1)
            snap_info_dict = dict(zip(keys, components))
            snap_info_dict['date'] = dt.now().isoformat()
            snap_info_list.append(snap_info_dict)

            mycursor.execute(insert_stmt2, tuple(snap_info_dict.values()))
            mydb.commit()


        return jsonify(snap_info_list)

    except subprocess.CalledProcessError as e:
        return str(e), 500

@app.route("/get-java-configs")
def get_java_configs():
    try:
        java_installed_output = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT, text=True)
        lines = java_installed_output.strip().split('\n')

        java_info_list = []

        for line in lines:
            if "openjdk version" in line:
                version = line.split('"')[1]
                if len(line.split('"')) > 2:
                    date_installed = line.split('"')[2]
            
            if "Environment" in line:
                components = re.split(r'\s+(?![^()]*\))', line)
                runtime_env_build=components[-1]

            if "VM" in line:
                server_VM_size=line.split(" ")[1]
                components = re.split(r'\s+(?![^()]*\))', line)
                VM_build=components[-1]
        
        java_info_dict = {
            "version": version,
            "date_installed": date_installed,
            "server_VM_size": server_VM_size,
            "runtime_env_build": runtime_env_build,
            "VM_build": VM_build,
            'date': dt.now().isoformat() 
        }

        java_info_list.append(java_info_dict)


        
        mycursor.execute(insert_stmt3, tuple(java_info_dict.values()))
        mydb.commit()

        return jsonify(java_info_list)

    except subprocess.CalledProcessError as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(port=8080, debug=True)
