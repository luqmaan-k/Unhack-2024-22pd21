import json

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
  # Handle dependencies in other function? step['dependency']

def findWafer(machine,wafers_unprocessed,steps):
  step_ids = []
  for step in steps:
    step_ids.append(step['id'])
  for idx,wafer in enumerate(wafers_unprocessed):
    for step_id in step_ids:
      if(wafer['processing_times'][step_id] > 0) and (step_id == machine['step_id']):
        return True,wafers_unprocessed.pop(idx)
  return False,None

def scheduleWafers(steps,machines,wafers):
  schedule = {}
  wafers_unprocessed = []
  wafers_processing  = []
  wafers_processed   = []
  
  # Covert the wafers to their wafer ids and store in an list containg unprocessed wafers for easier processing 
  for wafer in wafers:
    for i in range(1,wafer['quantity']+1):
      wafers_unprocessed.append({"wafer_id":wafer['type']+"-"+str(i),"processing_times":wafer["processing_times"]})
  available_machines  = [] # Each machine has a time from which it is available
  cooldown_machines   = [] # Each machine has a time when it went into cooldown
  processing_machines = [] # Each machine has a wafer id in it
  # Initialise the machines
  for machine in machines:
    if(checkIfNeedCooldown(machine,steps)):
      cooldown_machines.append([machine,0])
    else:
      available_machines.append([machine,0])
  # print("Available Machines :",available_machines)
  # print("Cooldown Machines  : ",cooldown_machines)

  while(wafers_unprocessed): # Keeps processing wafers until there are no unprocessed wafers
    print("Processing")
    # For each available machine find a wafer if possible then allocate
    for idx,available_machine in enumerate(available_machines):
      canAssign , wafer_to_assign = findWafer(available_machine[0],wafers_unprocessed,steps)
      # if canAssign:
      #   print("Can assign wafer ",wafer," to ",available_machine)
    
    # Do i have to do this?
    # Update the available_machine  list 
    for idx,available_machine in enumerate(available_machines):
      break

    # Update the cooldown_machine   list 
    for idx,available_machine in enumerate(available_machines):
      # Most prob dont have to do this and directly update it into the available machine list      
      break

    # Update the processing_machine list
    for idx,processing_machine in enumerate(processing_machines):
      # Might or might not have to do this and directly update it into the available machine list
      break

    break
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
