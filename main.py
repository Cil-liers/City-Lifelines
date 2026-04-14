# File that processes input for City Lifelines problem

import sys
import clingo

FACTS_FILE = "facts.lp"

def process_file(filename):
    with open(filename, "r") as file:
        first_line = True 
        number_of_edges = 0
        request_id = 1 


        for line in file:
            if first_line:
                lst = line.split()
                number_of_edges = int(lst[1])
                first_line = False


            elif number_of_edges != 0:
                edge = list(map(int, line.split()))
                with open(FACTS_FILE, "a") as new_file:
                    string1 = f"edge({edge[0]},{edge[1]}).\n"
                    string2 = f"edge({edge[1]},{edge[0]}).\n"
                    new_file.write(string1)
                    new_file.write(string2)
                number_of_edges -= 1


            else:
                request = list(map(int, line.split()))
                with open(FACTS_FILE, "a") as new_file:
                    string = f"request({request_id},{request[0]},{request[1]}).\n"
                    new_file.write(string)
                request_id += 1


def clear_file(filename):
    with open(filename, "w") as file:
        pass



def process_result(result, filename):
    number_served = 0
    route = ""
    current_id = 0

    clear_file(filename)

    for i in result:
        item = str(i)
        if "chosen" in item:
            number_served += 1

        elif "use" in item:
            item = item.replace(","," ") 
            item = item.replace("use(", "")
            item = item.replace(")", "")
            item = list(map(int, item.split()))

            request_id = item[0]

            start = item[1]
            end = item[2]

            if current_id == 0:
                current_id = request_id

            if current_id != request_id:
                with open(filename, "a") as file:
                    file.write("\n")
                route = ""
                current_id = request_id

            route = f"{start} -> {end}\n"
            with open (filename, "a") as file:
                file.write(route)

    with open (filename, "a") as file:
        file.write("\n")
        file.write(f"The maximum number of requests served is {number_served}")

        
def main():
    input_file = sys.argv[1]
    index = input_file.index(".")

    clear_file(FACTS_FILE)
    process_file(input_file)

    control = clingo.Control()

    control.load(FACTS_FILE)
    control.load("code.lp")

    control.ground([("base", [])])
    
    answer = [] 
    with control.solve(yield_=True) as handle:
        for model in handle:
            answer = list(model.symbols(shown=True))
    new_filename = f"output_{input_file[:index]}.txt"
    process_result(answer, new_filename)
if __name__ == "__main__":
    main()
