from maquinas.generic.machine import Machine

# Simulator class to handle multiple machines
class MachineSimulator:
    def __init__(self):
        self.machines = []

    def execute_machine(self, machine, data, entrada):
        """Execute the given machine directly."""
        if isinstance(machine, Machine):
            machine.start(data, entrada)
        else:
            print("Error: Only objects of type 'Machine' can be executed.")