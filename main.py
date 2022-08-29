from jeanice import Jeanice

destinations = ['-7.422743,109.179027', '-6.960964,107.567216', '-6.238389,106.829998',
                '-7.685202,109.041653', '-6.353464,107.239746', '-6.763633,108.518798',
                '-7.054489,110.433123', '-7.312553,112.711822', '-7.388220,110.569484',
                '-7.710929,110.355478', '-7.693007,109.692359']
jeanice = Jeanice(destinations=destinations, capacity=700, efficiency=16, max_duration=24, petrol_price=10000)

solution = jeanice.haleluya()
print('Solution:', solution['solution'])
print('Distance:', solution['distance'])
print('Petrol price:', f"Rp{solution['petrol_price']:,}")
print('Reduction:', solution['reduction'], '%')

