import json

def optimalMapping(milestone):
    steps = milestone['steps']
    machines = milestone['machines']
    wafers = milestone['wafers']
    solution = {}
    wafers_schedule = []
    for i in range(1,3):
      schedule_mapping = {}
      schedule_mapping['wafer_id'] = "W1"+"-"+ str(i)
      schedule_mapping['step'] = "" + str(i)
      schedule_mapping['machine'] = "M" + str(i)
      schedule_mapping['start_time'] = 5
      schedule_mapping['end_time'] = 5
      wafers_schedule.append(schedule_mapping)
    solution['schedule'] = wafers_schedule    
    return solution

def readFromFile(milestone_name):
  with open("Workshop_Problem/MilestoneInputs/"+milestone_name+".json","r") as inputfile:
    jsonload = json.load(inputfile)
  print(jsonload)
  return jsonload

def writeToFile(sol_for_milestone,milestone_name):
  with open("Workshop_Solution/MilestoneOutput/"+milestone_name+"_schedule"+".json","w") as outputfile:
    json.dump(sol_for_milestone,outputfile,indent=4,separators=(",",":"))

def runForMilestone(milestone_name):
    milestone = readFromFile(milestone_name)
    sol_for_milestone = optimalMapping(milestone)
    writeToFile(sol_for_milestone,milestone_name)


runForMilestone("Milestone0")
runForMilestone("Milestone1")
runForMilestone("Milestone2a")
runForMilestone("Milestone2b")
runForMilestone("Milestone3a")
runForMilestone("Milestone3b")
runForMilestone("Milestone3c")
runForMilestone("Milestone4a")
runForMilestone("Milestone4b")
runForMilestone("Milestone4c")
runForMilestone("Milestone5a")
runForMilestone("Milestone5b")
