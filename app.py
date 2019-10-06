from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys

#initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soda_machines.db'
db = SQLAlchemy(app)

# Declaring models and Column types Ref:
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#simple-example
class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String)
    machine_capacity = db.Column(db.Integer)
    sodas = db.Column(db.String)

    def __init__(self, machine_name, machine_capacity, sodas):
        self.machine_name = machine_name
        self.machine_capacity = machine_capacity
        self.sodas = sodas

# Function for handling new machine creation on the db
def create_machine(new_name, new_capacity, new_sodas):
    # Strip white spaces in names
    new_name = new_name.strip()

    # Check if a machine with that name exists already
    check_name = Machine.query.filter_by(machine_name=new_name).first()
    if check_name is not None:
        return "A machine with that name exists, try a different name"

    # Check if name has alphanumeric characters in machine name
    if any(char.isalpha() or char.isdigit() for char in new_name):
        #Check if capacity is numeric
        try:
            new_capacity = int(new_capacity)
        except:
            return "Capacity must be numeric"
        #Check if defined capacity is between 8 and 12
        if (7<new_capacity<13):
            # Check if sodas list has any elements
            if len(new_sodas.strip()):
                sodas = [s.strip() for s in new_sodas.split(",")]
                # Check if soda names have alphanumeric values in them
                for soda in sodas:
                    if not any(char.isalpha() or char.isdigit() for char in soda):
                        return "Soda names must contain letters and/or numbers"
                # Check if sodas are repeated and add a suffix
                sodas = list(map(lambda x: x[1] + "_" + str(sodas[:x[0]].count(x[1]) + 1) if sodas.count(x[1]) > 1 else x[1], enumerate(sodas)))
                # Check if sodas list exceeds capacity
                if len(sodas)<new_capacity:
                    new_sodas = ", ".join(sodas)
                else:
                    return "Soda capacity limited to %d"%new_capacity
        else:
            return "Machine Capacity must be 8<=capacity<=12"
    else:
        return "Machine names must contain letters and/or numbers"

    # create a new record with the given inputs
    machine = Machine(new_name, new_capacity, new_sodas)
    # add record to db
    db.session.add(machine)
    db.session.commit()
    return machine


#Function for removing machines
def delete_machine(machine_name):
    #Check if name exists in the Machine table
    check_machine = Machine.query.filter_by(machine_name=machine_name).first()
    if check_machine:
        db.session.delete(check_machine)
        db.session.commit()
        return True
    return False


#Function for adding sodas
def add_sodas(machine_name, new_sodas):
    check_machine = Machine.query.filter_by(machine_name=machine_name).first()
    sodas_list = [s.strip() for s in (check_machine.sodas).split(",")]
    new_sodas_list = [s.strip() for s in new_sodas.split(",")]

    #Check if machine already at capacity
    if len(sodas_list) == check_machine.machine_capacity:
        return "Machine already at max capacity, remove some sodas before adding new ones"
    #Check if current addition will exceed capacity
    if len(sodas_list)+len(new_sodas_list) > check_machine.machine_capacity:
        return "Can't add that many sodas, machine will exceed capacity. Remove some sodas first"
    # In order to avoid a blank element in the list
    if len(check_machine.sodas):
        sodas = sodas_list+new_sodas_list
    else:
        sodas = new_sodas_list

    # Add suffix for repeated sodas
    sodas = list(map(lambda x: x[1] + "_" + str(sodas[:x[0]].count(x[1]) + 1) if sodas.count(x[1]) > 1 else x[1], enumerate(sodas)))
    sodas = ", ".join(sodas)
    check_machine.sodas = sodas
    db.session.commit()
    return "success"

# Remove Sodas
def delete_sodas(machine_name, pop_sodas):
    check_machine = Machine.query.filter_by(machine_name=machine_name).first()
    # Compare sodas lists and see which sodas can be removed
    sodas_set = set([s.strip() for s in (check_machine.sodas).split(",")])
    pop_sodas_set = set([s.strip() for s in pop_sodas.split(",")])
    sodas = ", ".join(list(sodas_set - pop_sodas_set))
    check_machine.sodas = sodas
    db.session.commit()
    # Check for left out sodas in input which cant be found in current load of sodas in the machine
    if len(pop_sodas_set-sodas_set):
        message = str(pop_sodas_set-sodas_set) + " not found in sodas list for this machine"
        return message
    return "success"

# Declaring views
@app.route('/')
def index():
    machines = Machine.query.all()
    return render_template('index.html', machines=machines)

@app.route('/addmachine', methods=['GET', 'POST'])
def addmachine():
    # render the basic template when GET method is called
    if request.method == 'GET':
        return render_template('addmachine.html')

    # this works for POST calls
    machine_name = request.form.get('name_field')
    machine_capacity = request.form.get('capacity_field')
    sodas = request.form.get('sodas_field')

    creation_response = create_machine(machine_name, machine_capacity, sodas)
    # Check for error calls vs success calls
    if isinstance(creation_response, str):
        error = creation_response
        machine = None
    else:
        error = None
        machine = creation_response
    return render_template('addmachine.html', machine=machine, error = error)

@app.route('/removemachine', methods=['GET', 'POST'])
def removemachine():
    if request.method == 'GET':
        machines = Machine.query.all()
        return render_template('removemachine.html', machines=machines)
    machine_name = (request.form.get('name_field'))
    deletion_reponse = delete_machine(machine_name)
    machines = Machine.query.all()
    if deletion_reponse:
        machine = machine_name
        error = None
    else:
        machine = None
        error = "No Machine found with that name"
    return render_template('removemachine.html', machines=machines, machine=machine, error = error)


@app.route('/addsodas', methods=['GET', 'POST'])
def addsodas():
    machines = Machine.query.all()
    if request.method == 'GET':
        return render_template('addsodas.html', machines = machines)

    machine_name = request.form.get('name_field')
    new_sodas = request.form.get('sodas_field')
    creation_response = add_sodas(machine_name, new_sodas)
    if creation_response=="success":
        error = None
        success = "Sodas added to machine successfully."
    else:
        error = creation_response
        success = None
    return render_template('addsodas.html', machines = machines, success=success, error = error)

@app.route('/removesodas', methods=['GET', 'POST'])
def removesodas():
    if request.method == 'GET':
        machines = Machine.query.all()
        return render_template('removesodas.html', machines=machines)
    machine_name = (request.form.get('name_field'))
    pop_sodas = request.form.get('sodas_field')
    deletion_reponse = delete_sodas(machine_name, pop_sodas)
    machines = Machine.query.all()
    if deletion_reponse=="success":
        success = "Sodas removed from machine successfully."
        error = None
    else:
        success = None
        error = deletion_reponse
    return render_template('removesodas.html', machines=machines, success=success, error = error)

# Check for create argument and create the db for the first run
try:
    if sys.argv[1]=='create':
        print("Creating database tables...")
        db.create_all()
        print("Done!")
except:
    pass

if __name__ == "__main__":
    app.run()
