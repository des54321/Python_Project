from sim_run import sim, Cell, interate
from grid_class import Grid
from random import randrange, random, randint
from copy import deepcopy



def give_score(obj):
    return obj.score


def random_rule():
    return [randint(-rule_max_dist,rule_max_dist),randint(-rule_max_dist,rule_max_dist),4*random()-2]


def make_datapoint(length):
    data = []
    start = (random()*20) - 10
    add = (random()*10) - 5
    add = round(add*100)/100
    start = round(start*100)/100
    for i in range(length):
        data.append(round(start*100)/100)
        start += add
    return data




class RuleAI:
    def __str__(self) -> str:
        return f'Rule: {self.rule}    Run Length: {self.run_length}    Score: {self.score}'



    def __init__(self) -> None:
        self.rule = [ random() - 0.5 , [0,0,2*random()-1]]
        for i in range(randint(1,10)):
            self.rule.append(random_rule())
        self.run_length = randint(2,6)
        self.score = 0
    

    def test_on(self, inputs, outputs, desired_outputs) -> float:
        ran_outputs = sim(self.rule, c_w, c_h, inputs, outputs, self.run_length)
        total = 0
        for i in range(len(ran_outputs)):
            diff = abs(ran_outputs[i] - desired_outputs[i])
            total += diff
        return total/len(ran_outputs)
    

    def vary_self(self):
        self.rule[0] += (random()-0.5)/15
        if random() < new_rule_chance:
            self.rule.append(random_rule())
        if random() < delete_rule_chance:
            del self.rule[randint(1,len(self.rule)-1)]
        for i in range(1,len(self.rule)):
            if random() < move_rule_chance:
                self.rule[i][0] += randint(-1,1)
            if random() < move_rule_chance:
                self.rule[i][1] += randint(-1,1)
            self.rule[i][2] += (random()-0.5)/8
        if random() < new_length_chance:
            self.run_length += randint(-1,1)
            if self.run_length < 1:
                self.run_length = 5

                










c_w = 9
c_h = 7
rule_max_dist = 4
max_value = 50
new_rule_chance = 0.4
delete_rule_chance = 0.2
move_rule_chance = 0.3
new_length_chance = 0.3
ai_num = 400
ai_duped = 25
database = []
inputs_pos = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0)]
outputs_pos = [(5,3)]
for i in range(8):
    database.append(make_datapoint(10))

wanted_outputs = []
final_inputs = []
for i in database:
    new_input = []
    for x in range(len(inputs_pos)):
        new_input.append(list(inputs_pos[x])+[i[x]])
    final_inputs.append(new_input)
    wanted_outputs.append([i[-1]])





test_ai = []
for i in range(ai_num):
    test_ai.append(RuleAI())

for n in range(1000):
    print(f'This is generation {n}!')
    for i in test_ai:
        scores = []
        for x in range(len(final_inputs)):
            scores.append(i.test_on(final_inputs[x],outputs_pos,wanted_outputs[x]))
        i.score = sum(scores)/len(scores)
    test_ai.sort(key=give_score)
    del test_ai[ai_duped:]
    for i in range(ai_num - 1):
        test_ai.append(deepcopy(test_ai[n%ai_duped]))
    for i in range(len(test_ai)):
        if i > ai_duped:
            test_ai[i].vary_self()
    print(test_ai[0].score)
    


        



print(f'''Learning is done,
this is what the best looks like:''')
print(test_ai[0])
