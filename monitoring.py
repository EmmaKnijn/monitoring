systems = []
menuOptions = [{"name":"Add System","key":"a","action": "add"},{"name": "Exit and print the data","key":"e", "action": "exit"}]

systemOptions = ["hostname","ip"]

while True:
    print("Select an option")
    for option in menuOptions:
        print(f"{option["key"]}: {option["name"]}")
    
    selection = input()

    selectedOption = None # initialise the variable here so it is accesible outside of the for loop

    # sins have been comitted
    for option in menuOptions: 
        if option["key"] == selection:
            selectedOption = option

    if selectedOption != None:
        
        if selectedOption["action"] == "exit":
            break
        elif selectedOption["action"] == "add":
            systemObject = {}
            for option in systemOptions:
                print(f"Enter value for property {option}:")
                systemObject[option] = input()
            
            systemObject["monitorables"] = []

            print("Enter your monitorables, enter `exit` to exit")

            while True:
                monitorable = input()
                if monitorable == "exit":
                    break
                systemObject["monitorables"].append(monitorable)


            systems.append(systemObject)

    

for system in systems:
    print(f"{system["hostname"]} ({system["ip"]}): {system["monitorables"]}")