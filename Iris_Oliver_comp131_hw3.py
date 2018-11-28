# Iris Oliver
# comp131 hw3
# Collaborated with: Cathy Cowell, Leah Stern

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# You are going on a hiking trip, and there is a limit to the things you can 
# bring. You have two things: a backpack with a size (the weight it can hold 
# that is) and a set of boxes with different weights and different importance 
# values. The goal is to fill the backpack to make it as valuable as possible 
# without exceeding the maximum weight (120). 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Sources:
# https://stackoverflow.com/questions/10879867/sum-average-an-attribute-of-
# 	a-list-of-objects-in-python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Instructions to run this program:
# Run the command:
# 
#		python Iris_Oliver_comp131_hw3.py
#
# Output will be 
#
# 		1. A list of the generations and the maximum values at each.
#		2. The population on the final generation - all of the chromosomes
#		3. The best chromosome and its weight and value. 
#

from __future__ import print_function
import random
import operator

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Used to create colors, reference 
# https://stackoverflow.com/questions/287871/print-in-terminal-with-colors
#
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Box
# Contains the information about one box: its weight, value, and whether or 
# not it is in the knapsack
#
class Box:
	def __init__(self, weight, value, inPack):
		self.weight = weight
		self.value = value
		self.inPack = inPack


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Chromosome
# Contains a list of 7 boxes, all of which start outside of the bag.
#
class Chromosome:
	def __init__(self):
		box1 = Box(20, 6, False)
		box2 = Box(30, 5, False)
		box3 = Box(60, 8, False)
		box4 = Box(90, 7, False)
		box5 = Box(50, 6, False)
		box6 = Box(70, 9, False)
		box7 = Box(30, 4, False)
		self.boxes = [box1, box2, box3, box4, box5, box6, box7]
		self.weight = 0
		self.value = 0

	# readChromosome outputs the boxes which are in the knapsack, the total 
	# weight, and the total value. 
	def readChromosome(self):
		for box in self.boxes:
			if box.inPack:
				print("Box weight:", box.weight, "| Box value:", box.value)
		print("Total weight:", self.weight)
		print("Total value:", self.value)
		print()

	# calcWeight returns the value of the given chromosome (the sum of the 
	# weights of all the boxes)
	def calcWeight(self):
		self.weight = sum(box.weight for box in self.boxes if box.inPack)
		return self.weight

	# calcValue returns the value of the given chromosome (the sum of the
	# values of all the boxes). If the weight of the Chromosome > 120, the value 
	# will be 0. 
	def calcValue(self):
		if (self.calcWeight() > 120):
			self.value = 0
		else:
			self.value = sum(box.value for box in self.boxes if box.inPack)
		return self.value

	# mutateChromosome changes a random selection of genes to the opposite of 
	# their previous values
	def mutateChromosome(self):
		numToMutate = random.randint(1, 7)
		for i in range(numToMutate):
			toMutate = random.randint(0, 6) # index of the box to change
			self.boxes[toMutate].inPack = not self.boxes[toMutate].inPack
		self.calcValue()
		self.calcWeight()

	# crosses over two chromosomes by replacing the first half of one with the
	# first half of the other. Returns the new child chromosome.
	def crossover(self, other):
		child = Chromosome()
		for i in range(7):
			if (i < 3):
				child.boxes[i].inPack = self.boxes[i].inPack
			else:
				child.boxes[i].inPack = other.boxes[i].inPack
		
		child.calcWeight()
		child.calcValue()
		return child


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Population
# A list of 8 chromosomes. 
#
class Population:

	# initializes the population of empty bag chromosomes. Pop size = 8.
	def __init__(self):
		self.chromosomes = []
		for i in range(8):
			self.chromosomes.append(Chromosome())

	# sorts the chromosomes in a population in ascending order by their 
	# value. Used to ascertain which chromosomes are the most fit. 
	def calcFitness(self):
		self.chromosomes.sort(key=operator.attrgetter('value'))

	# mutates one random chromosome in the population
	def mutatePop(self):
		toMutate = random.randint(0,7) 	# index of the chromosome to mutate
		self.chromosomes[toMutate].mutateChromosome()
	
	# mates the four fittest individuals of the population (the top half of the 
	# chromosomes array) to create 4 new children. Deletes the lowest half of
	# the array (inferior half of the population) and appends the four new 
	# children. 
	def reproduce(self):
		self.calcFitness()

		child1 = self.chromosomes[4].crossover(self.chromosomes[5])
		child2 = self.chromosomes[4].crossover(self.chromosomes[6])
		child3 = self.chromosomes[5].crossover(self.chromosomes[7])
		child4 = self.chromosomes[5].crossover(self.chromosomes[7])

		del self.chromosomes[:4]
		self.chromosomes.extend([child1, child2, child3, child4])
	
	# prints out the entire population
	def printPopulation(self):
		count = 0
		for chromosome in self.chromosomes:
			print("Chromosome number: ", count)
			print("Boxes in the chromosome: ")
			chromosome.readChromosome()
			count += 1

	# prints the best chromosome in the array (the chromosome with the highest
	# value)
	def printBest(self):
		self.calcFitness()
		self.chromosomes[7].readChromosome()

	# prints a summary of the population
	def printPopSummary(self):
		self.calcFitness()
		print("Best weight:", self.chromosomes[7].weight, 
				"| Best height:", self.chromosomes[7].value)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# controls the entire genetic algorithm. Runs the algorithm for 40 generations.
# Prints and displays information about different generations. 
#
def geneticAlgorithm():
	initPop = Population()

	for numGenerations in range(40):
		print(color.BLUE, color.BOLD, "Generation ", numGenerations, ": ", 
					color.END, sep="", end="")

		initPop.printPopSummary()
		initPop.calcFitness()
		initPop.reproduce()
		initPop.mutatePop()
	
	print()
	print(color.RED, color.BOLD, "FINAL POPULATION", color.END, sep="")
	initPop.printPopulation()
	print(color.RED, color.BOLD, "BEST CHROMOSOME", sep="")
	initPop.printBest()
	print(color.END, end="")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# run the above code
geneticAlgorithm()
