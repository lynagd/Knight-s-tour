import random
from src.population import Population

def run_single_attempt(max_gen=1000, silent=True):
    """Run algorithm once and return result"""
    population = Population(50)
    
    for _ in range(max_gen):
        population.check_population()
        max_fitness, best = population.evaluate()
        
        if not silent and population.generation % 100 == 0:
            print(f"  Gen {population.generation}: Fitness {max_fitness}")
        
        if max_fitness == 64:
            return {
                'success': True,
                'generations': population.generation,
                'fitness': 64
            }
        
        population.create_new_generation()
    
    # Failed - return best achieved
    return {
        'success': False,
        'generations': max_gen,
        'fitness': max_fitness
    }

def main():
    """Test success rate over 10 runs"""
    print("=" * 60)
    print("TESTING SUCCESS RATE (10 runs)")
    print("=" * 60)
    
    results = []
    
    for run in range(1, 11):
        print(f"\nRun {run}/10:", end=" ")
        result = run_single_attempt(max_gen=1000, silent=True)
        results.append(result)
        
        if result['success']:
            print(f"✅ SUCCESS in {result['generations']} generations")
        else:
            print(f"❌ FAILED (best fitness: {result['fitness']}/64)")
    
    # Statistics
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    successes = [r for r in results if r['success']]
    failures = [r for r in results if not r['success']]
    
    success_rate = len(successes) / len(results) * 100
    print(f"\nSuccess Rate: {len(successes)}/10 ({success_rate:.0f}%)")
    
    if successes:
        avg_gens = sum(r['generations'] for r in successes) / len(successes)
        min_gens = min(r['generations'] for r in successes)
        max_gens = max(r['generations'] for r in successes)
        print(f"\nWhen successful:")
        print(f"  Average generations: {avg_gens:.1f}")
        print(f"  Fastest: {min_gens} generations")
        print(f"  Slowest: {max_gens} generations")
    
    if failures:
        avg_fitness = sum(r['fitness'] for r in failures) / len(failures)
        print(f"\nWhen failed:")
        print(f"  Average best fitness: {avg_fitness:.1f}/64")
        best_failure = max(r['fitness'] for r in failures)
        print(f"  Closest attempt: {best_failure}/64")
    
    print("\n" + "=" * 60)
    
    # Recommendation
    if success_rate >= 80:
        print("✅ Success rate is good! No changes needed.")
    elif success_rate >= 50:
        print("⚠️  Success rate is okay. Consider:")
        print("   - Increase population_size to 70-100")
        print("   - Or run multiple attempts")
    else:
        print("❌ Success rate is low. Recommend:")
        print("   - Increase population_size to 100")
        print("   - Increase max_generations to 2000")
        print("   - Or increase mutation rate to 0.02")
    
    print("=" * 60)

if __name__ == "__main__":
    main()