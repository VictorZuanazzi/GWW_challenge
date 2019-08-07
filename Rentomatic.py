# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:11:23 2019

@author: Victor Zuanazzi
"""

class Rental:
    def __init__(self, start_date, vehicle):
        """Class to keep the state of the rental"""
        self.start_date = start_date
        self.vehicle = vehicle
        self.returned = False
        
class Inventory:
    """Class to keep the inventory"""
    def __init__(self):
        
        self.transport_types = {'bike', 'car', 'motorbike', 'boat'}
        self.price = {'bike': 1, 'car': 100, 'motorbike': 10, 'boat': 1000}
        self._total = {'bike': 10, 'car': 10, 'motorbike': 10, 'boat': 10}
        self.num_available = self._total.copy()
        self.rentals= {}
        self.all_rents_in_history = 0
        
        
    def list_of_vehicles(self):
        """returns the list of vehicles"""
        return self.transport_types
    
    def give_info(self, vehicle):
        """give the information regarding one specific transport type. 
        This logic does not scale for an arbitrary number of information.
        inptu:
            vehicle: string, one of the transport_types
        return: int tuple, (price, num_available)"""
        return self.price[vehicle], self.num_available[vehicle]
    
    def rent_a_vehicle(self, vehicle, start_date):
        """process the rent of a vehicle.
        input:
            vehicle: string, one of the transport_types
            start_date: int, a number between 1 and 365 making the day of the 
                year. (that is only done to simplify the logic)
        output: 
            bool, False if the rent is not possible.
            integer, protoco_number
        """
        
        if self.num_available[vehicle] == 0:
            print(f"There is no {vehicle} of this type left")
            return False
        
        self.num_available[vehicle] -= 1
        self.all_rents_in_history +=1
        protocol_number = self.all_rents_in_history
        
        self.rentals[protocol_number] = Rental(int(start_date), vehicle)
        
        return protocol_number
    
    def pay_rental(self, protocol_number, end_date):
        """defines the amount to be paid and process the return of the vehicle.
        input:
            protocol_number: int (or numeric string), containing the protocol 
                number of the rental
            end_date: int, the return date, assumed to be higher than the start
                date. Number between 0 and 356."""
        
        protocol_number = int(protocol_number)
        end_date = int(end_date)
        
        if protocol_number not in self.rentals:
            print("This protocol number does not exist")
            return False
        
        if self.rentals[protocol_number].returned:
            print("This vehicle was already returned")
            return False
        else:
            self.rentals[protocol_number].returned = True
        
        vehicle = self.rentals[protocol_number].vehicle
        start_date = self.rentals[protocol_number].start_date
        
        to_pay = (end_date - start_date) *  self.price[vehicle]
        
        self.num_available[vehicle] += 1 
        return to_pay
        

def main():
    
    
    inventory = Inventory()
    
    
    actions = {"help", 
               "list of all vehicles", 
               "info about specific vehicle",
               "rent a vehicle", 
               "pay rental costs",
               "exit"}
    
    act_help = {"help": "provides information about all options", 
               "list of all vehicles": "returns the list of vehicles", 
               "info about specific vehicle": "gives the information of a specific transport type",
               "rent a vehicle": "rent a vehicle of choosing", 
               "pay rental costs": "pays for the rental of the vehicle",
               "exit": "terminates the program"}
    
    
    while True:
        action = input(f"Select one action: {actions} \n")
    
        if action not in actions:
            print("The input does is not a supported action.")
            continue
        
        if action == "help":
            print("You have the following options:")
            for key in act_help:
                print(f"\t {key}: {act_help[key]}")
        
        if action == 'list of all vehicles':
            print(f"{inventory.list_of_vehicles()}")
            continue
        
        if action == 'info about specific vehicle':
            vehicle = input("Which vehicle do you want to know more about? \n")
            info = inventory.give_info(vehicle)
            print(f"{vehicle}: \n\t price: {info[0]}, \n\t available units: {info[1]}")
            continue
        
        if action == "rent a vehicle":
            vehicle = input(f"Which vehicle do you want to rent? {inventory.list_of_vehicles()}\n")
            start_date = input("When Would you like to rent it? " + 
                               "Please, give a number between 0 and 365" + 
                               " correspondent to the day of the year. \n")
            protocol_number = inventory.rent_a_vehicle(vehicle, start_date)
            if protocol_number > 0:
                print(f"You successfuly rented the {vehicle} at {start_date}")
                print(f"Your protocol number is: {protocol_number}. " + 
                      "You will need this number in order to return the vehicle.")
                
        if action == "pay rental costs":
            protocol_number = input(f"Please provide your protocol number. \n")
            end_date = input(f"Please, provide the date the rent ends. \n" + 
                             "Please, give a number between 0 and 365" + 
                             " correspondent to the day of the year. \n")

            to_pay = inventory.pay_rental(protocol_number, end_date)
            
            if to_pay > 0:
                print(f"Your rental bill is of EUR {to_pay}.")
        
        if action == "exit":
            print("This session will be terminated")
            break

if __name__ == '__main__':
    main()