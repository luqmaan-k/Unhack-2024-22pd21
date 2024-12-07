import json
import copy
def writeSchedulePlan():
  wafers_schedule = []
  for i in range(1,3):
    schedule_mapping = {}
    schedule_mapping['wafer_id'] = "W1"+"-"+ str(i)
    schedule_mapping['step'] = "S" + str(i)
    schedule_mapping['machine'] = "M" + str(i)
    schedule_mapping['start_time'] = 5
    schedule_mapping['end_time'] = 5
    wafers_schedule.append(schedule_mapping)
  return wafers_schedule

# Check whether the machine needs a cooldown
def checkIfNeedCooldown(machine,steps):
  for step in steps:
    if(step['id'] == machine['step_id']):
      if(machine['initial_parameters']['P1'] in range(step['parameters']['P1'][0],step['parameters']['P1'][1]+1)):
        return False
      else:
        return True
  # Handle dependencies in other function? step['dependency'] or maybe here

def findWafer(machine,wafers_unprocessed,steps):
  step_ids = []
  print(wafers_unprocessed)
  for step in steps:
    step_ids.append(step['id'])
  for idx,wafer in enumerate(wafers_unprocessed):
    if (machine['step_id'] in  wafer['processing_times']) :
      if (wafer['processing_times'][machine['step_id']] > 0):
        print("Wafer : ",wafer)
        print("Allocated to : ",machine)
        return True,wafers_unprocessed.pop(idx)
  return False,None

def machineProcess(processing_machine):
  #  Returns Modified machine (initial_parameter modified,n decreased), the new available time of the machine , the modified wafer 
  modified_machine = processing_machine[0]
  available_time   = processing_machine[1]
  modified_wafer   = processing_machine[2]

  machine_stage = modified_machine['step_id']

  modified_machine['n'] = modified_machine['n'] - 1
  # if n == 0?
  for key in modified_machine['initial_parameters']:
    modified_machine['initial_parameters'][key] += modified_machine["fluctuation"][key]
  available_time  = available_time + modified_wafer["processing_times"][machine_stage]

  print("-------",machine_stage)
  print("++++++++++++",modified_wafer['processing_times'][machine_stage])
  del modified_wafer['processing_times'][machine_stage]
  # Maybe Handle dependecy here???

  print("Processed :-")
  print("Modified Machine : ",modified_machine)
  print("Modified Wafer",modified_wafer)
  print(available_time)

  return modified_machine,available_time,modified_wafer

def machineCooldown(cooldown_machine,allmachines):
  # Returns the modified machines after cooldown
  modified_machine = cooldown_machine[0]
  available_time   = cooldown_machine[1]
  temp_machine_id = cooldown_machine['machine_id']

  available_time += modified_machine['cooldown_time']

  for machine in allmachines :
    if machine['machine_id'] == temp_machine_id :
      modified_machine['n'] = machine['n']

  return modified_machine,available_time

def scheduleWafers(steps,machines,wafers):
  schedule = {}
  wafers_unprocessed = []
  wafers_processing  = []
  wafers_processed   = []
  
  # Covert the wafers to their wafer ids and store in an list containg unprocessed wafers for easier processing 
  for wafer in wafers:
    for i in range(1,wafer['quantity']+1):
      wafers_unprocessed.append({"wafer_id":wafer['type']+"-"+str(i),"processing_times":copy.deepcopy(wafer["processing_times"])})
  for i in wafers_unprocessed:
    print(i)
  available_machines  = [] # Each machine has a time from which it is available
  cooldown_machines   = [] # Each machine has a time when it went into cooldown
  processing_machines = [] # Each machine has a wafer id with it
  # Initialise the machines
  for machine in machines:
    if(checkIfNeedCooldown(machine,steps)):
      cooldown_machines.append([machine,0])
    else:
      available_machines.append([machine,0])
  # print("Available Machines :",available_machines)
  # print("Cooldown Machines  : ",cooldown_machines)

  while(wafers_unprocessed): # Keeps processing wafers until there are no unprocessed wafers
    print("\n---------------Processing----------------")
    # For each available machine find a wafer if possible then allocate
    for idx,available_machine in enumerate(available_machines):
      canAssign , wafer_to_assign = findWafer(available_machine[0],wafers_unprocessed,steps)
      if canAssign:
        machine_temp = available_machines.pop(idx)
        processing_machines.append( [machine_temp[0],machine_temp[1],wafer_to_assign] )
    
    # Update the processing_machine list
    print("Processing Machines : ",processing_machines)
    for idx,processing_machine in enumerate(processing_machines):
      print("Processing Machine is : " , processing_machine)
      modified_machine , new_available_time,modified_wafer = machineProcess(processing_machine)
      print("Wafers status after modification : ",wafers_unprocessed)
      if(checkIfNeedCooldown(machine,steps)):
        cooldown_machines.append([modified_machine,new_available_time])
      else:
        available_machines.append([modified_machine,new_available_time])
      # If wafer is done then send it to processed
      if(modified_wafer['processing_times']):
        print("Appending non empty wafer",modified_wafer)
        wafers_unprocessed.append(modified_wafer)
      else :
        wafers_processed.append(modified_wafer)
    processing_machines = []
    # Update the cooldown_machine list 
    for idx,cooldown_machine in enumerate(cooldown_machines):
      modified_machine , new_available_time = machineCooldown(cooldown_machine,machines)
      available_machines.append([modified_machine,new_available_time])
    cooldown_machines = []
  # print(wafers_unprocessed)
  return writeSchedulePlan()

def optimalMapping(milestone):
  steps = milestone['steps']
  machines = milestone['machines']
  wafers = milestone['wafers']
  solution = {}
  solution['schedule'] = scheduleWafers(steps,machines,wafers)    
  return solution

def readFromFile(milestone_name):
  with open("Workshop_Problem/MilestoneInputs/"+milestone_name+".json","r") as inputfile:
    jsonload = json.load(inputfile)
  # print(jsonload)
  return jsonload

def writeToFile(sol_for_milestone,milestone_name):
  with open("Workshop_Solution/MilestoneOutput/"+milestone_name+"_schedule"+".json","w") as outputfile:
    json.dump(sol_for_milestone,outputfile,indent=4,separators=(",",":"))

def runForMilestone(milestone_name):
  milestone = readFromFile(milestone_name)
  sol_for_milestone = optimalMapping(milestone)
  writeToFile(sol_for_milestone,milestone_name)


runForMilestone("Milestone0")
# runForMilestone("Milestone1")
# runForMilestone("Milestone2a")
# runForMilestone("Milestone2b")
# runForMilestone("Milestone3a")
# runForMilestone("Milestone3b")
# runForMilestone("Milestone3c")
# runForMilestone("Milestone4a")
# runForMilestone("Milestone4b")
# runForMilestone("Milestone4c")
# runForMilestone("Milestone5a")
# runForMilestone("Milestone5b")
