from abc import ABC, abstractmethod
from maquinas.machine import Machine

# Simulator class to handle multiple machines
class MachineSimulator:
    def __init__(self):
        self.machines = []

    def add_machine(self, machine):
        if isinstance(machine, Machine):
            self.machines.append(machine)
        else:
            print("Error: Only objects of type 'Machine' can be added.")

    def run_simulation(self):
        for machine in self.machines:
            print(f"\nSimulating {machine.name}:")
            data = machine.read_json("maquinas/AP/Jsons/inic-a.json")
            machine.start(data, "AAAAAabbB")