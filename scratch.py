from christine import Christine
from dotenv import load_dotenv

load_dotenv()
destinations = ['-7.422743,109.179027', '-6.960964,107.567216', '-6.238389,106.829998',
                '-7.685202,109.041653', '-6.353464,107.239746', '-6.763633,108.518798',
                '-7.054489,110.433123', '-7.312553,112.711822', '-7.388220,110.569484',
                '-7.710929,110.355478', '-7.693007,109.692359']

solutions = [0, 3, 2, 0]

christine = Christine(destinations, solutions, 10)

print('time', christine.haleluya())
