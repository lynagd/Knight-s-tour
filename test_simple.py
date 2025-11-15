from src.chromosome import Chromosome
from src.knight import Knight
from src.population import Population

print("Testing Chromosome...")
chr1 = Chromosome()
print(f"✅ Chromosome created: {chr1}")

print("\nTesting Knight...")
knight = Knight()
print(f"✅ Knight created: {knight}")

print("\nTesting Population...")
pop = Population(5)
print(f"✅ Population created")

print("\nTesting check_moves...")
pop.check_population()
print("✅ Check moves completed")

print("\nTesting evaluation...")
max_fit, best = pop.evaluate()
print(f"✅ Best fitness: {max_fit}")

print("\n🎉 All tests passed!")