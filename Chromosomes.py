import random
import copy

class Chromosome:

    def change_body(self,body):
        # body = bin(body)[2:]
        # self._body = (self._lenght - len(body))*'0' + body
        # self._body_list = list(self._body)
        if type(body) == str and len(body) == self._lenght:
            try:
                int(body,2)
            except ValueError as e:
                raise ValueError("Invalid string") from e
            finally:
                self._body = (self._lenght - len(body))*'0' + body
                self._body_list = list(self._body)
        elif type(body) == int and body < 2**self._lenght:
            try:
                body = bin(body)[2:]
                self._body = (self._lenght - len(body))*'0' + body
                self._body_list = list(self._body)
            except Exception as e:
                raise Exception from e
        else:
            raise ValueError("Incorrect value for chromosome generation")

    def __init__(self,body,lenght):
        self.value = 0
        self.weight = 0
        try:
            self._lenght = int(lenght)
        except ValueError as e:
            raise ValueError(f"Invalind lenght value {e}") from e
        self.change_body(body)

    def get_ch(self):
        return self._body

    def get_ch_list(self):
        return self._body_list

    def print_ch(self):
        print(self.get_ch())

    def print_ch_list(self):
        print(self.get_ch_list())

    def to_int(self):
        return int(self._body,2)

        # self._body =  bin(random.randint(0,2**self._lenght))[2:]
        # self._body = (self._lenght - len(self._body))*'0' + self._body
        # self._body_list = list(self._body)

    def set_value(self,value):
        self.value = value

    def set_weight(self,weight):
        self.weight = weight

    def random_trashing(self):
        for i,_ in enumerate(self._body_list):
            if self._body_list[i] == '1' and bool(random.getrandbits(1)):
                # print(f'Before trashing {self._body_list}')
                self._body_list[i] = '0'
                # print(f'After trashing {self._body_list}')
                break
        self.change_body(''.join(self._body_list))
        self.set_weight(calculateWeight(self))

    def mutate(self):
        chnum = random.randint(0,self._lenght-1)
        body_list = self.get_ch_list()
        body_list[chnum] = str(1 - int(body_list[chnum])) # change from 1 to 0 and other way
        self.change_body(''.join(body_list))

    # def __eq__(self,other):
    #     return self.value == other.value

def generateWeight(lenght):
    # weight = []
    # for _ in range(lenght):
    #     weight.append(int(input()))
    return [5,7,13,9,2,20,18,4,8,6]

def generateValues(lenght):
    # values = []
    # for _ in range(lenght):
    #     values.append(int(input()))
    return [12,33,21,7,10,5,14,8,11,4]

def generateChomosomes(num,lenght):
    chromosomes = []
    for _ in range(num):
        chromosomes.append(Chromosome(random.randint(0,2**lenght-1),lenght))
    setParams(chromosomes)
    return chromosomes

def calculateValue(chromosome):
    return sum(int(a)*b for a,b in zip(chromosome.get_ch_list(),values))

def calculateWeight(chromosome):
    return sum(int(a)*b for a,b in zip(chromosome.get_ch_list(),weights))

# def random_trashing(chromosome):
#     for i, _ in enumerate(chromosome)

def correctWeight(chromosomes):
    for chromosome in chromosomes:
        weight = chromosome.weight
        while weight > max_weight:
            weight = chromosome.weight
            chromosome.random_trashing()
    setParams(chromosomes)

def setParams(chromosomes):
    for chromosome in chromosomes:
        chromosome.set_value(calculateValue(chromosome))
        chromosome.set_weight(calculateWeight(chromosome))

# def checkChromosomes(lis):
#     correctWeight(lis,weights)
#     setParams(lis)
    # for i,chromosome in enumerate(lis):
    #     chromosome.set_weight(calculateWeight(chromosome,weights))
    #     chromosome.set_value(calculateValue(chromosome,values))
        # print(f'Ch({i+1}) weight = {chromosome.weight}')
        # print(f'Ch({i+1}) value = {chromosome.value}')
        # print('_'.center(50,'_'))

def sumofweight(chromosomes):
    return sum(chromosome.weight for chromosome in chromosomes)

def sumofvalues(chromosomes):
    return sum(chromosome.value for chromosome in chromosomes)

def selection(chromosomes):
    chromosomes_copy = copy.deepcopy(chromosomes)
    sumofv = sumofvalues(chromosomes)
    chancesofrulett = {i+1:(chromosomes.value / sumofv * 100) for i,chromosomes in enumerate(chromosomes)}
    temp = 0
    for i,chance in enumerate(chancesofrulett.values()):
        if i == 0:
            temp = chance
            continue
        temp += chance
        chancesofrulett[i+1] = temp
    for chromosome in chromosomes:
        choice = (random.random()*100 % 100)
        # print(f'choice = {choice}')
        for key in chancesofrulett:
            # print(value)
            if choice <= chancesofrulett[key]:
                # print(key)
                chromosome.change_body(chromosomes_copy[key-1].get_ch())
                break

def crossing(chromosomes):
    for i in range(0,len(chromosomes),2):
        Pk_cof = random.random()
        if Pk_cof < Pk:
            chnum = random.randint(1,chromosomes_lenght-1)
            first = chromosomes[i].get_ch()
            second = chromosomes[i+1].get_ch()
            chromosomes[i].change_body(first[chnum:] + second[:chnum])
            chromosomes[i+1].change_body(second[chnum:] + first[:chnum])
            # print(f'{chnum=} {first[chnum:]}')

def mutation(chromosomes):
    for chromosome in chromosomes:
        Pm_cof = random.random()
        if Pm_cof < Pm:
            chromosome.mutate()
            # print('Mutation')


def pr(lis):
    for i,j in enumerate(lis):
        print(f'Ch({i+1}) = {j.get_ch_list()}')
        print(f'Ch({i+1}) Value: {j.value}; Weight: {j.weight}')

def printresults(chromosomes):
    print('Resulting generation'.center(58,'-'),end="\n\n")
    pr(chromosomes)
    print(f'Sum of values = {sumofvalues(chromosomes)}; Weight = {sumofweight(chromosomes)}')
    print(''.center(58,'-'),end='\n\n')

if __name__ == "__main__":
    max_weight = 58
    Pk = 0.8
    Pm = 0.1
    number_of_chromosomes = 6
    chromosomes_lenght = 10

    weights = [5,7,13,9,2,20,18,4,8,6]
    values = [12,33,21,7,10,5,14,8,11,4]

    print()
    print('Creating first generation'.center(58,'-'),end="\n\n")
    chromosomes = generateChomosomes(number_of_chromosomes,chromosomes_lenght)
    correctWeight(chromosomes)
    # checkChromosomes(chromosomes)
    pr(chromosomes)
    print(''.center(58,'-'),end='\n\n')

    def startAlgorithm():
        selection(chromosomes)
        crossing(chromosomes)
        mutation(chromosomes)
        correctWeight(chromosomes)

    def solving_loop():
        counter = 0
        while counter < 8:
            sum_prev = sumofvalues(chromosomes)
            startAlgorithm()
            sum_now = sumofvalues(chromosomes)
            if sum_prev <= sum_now:
                counter += 1
            else:
                counter = 0
        printresults(chromosomes)

    solving_loop()
