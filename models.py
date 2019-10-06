from app import db

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

if __name__ == '__main__':
    print("Creating database tables...")
    db.create_all()
    print("Done!")
