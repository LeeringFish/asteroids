import os.path

class ScoreManager():
    FILENAME = "./highscore.txt"
    
    def __init__(self):
        self.high_score = self.read_high_score()
        self.current_score = 0

    def add_point(self):
        self.current_score += 1

    def read_high_score(self):
        if os.path.isfile(self.FILENAME):
            with open(self.FILENAME) as file:
                score = file.read().strip()
                try:
                    return int(score)
                except ValueError:
                    return 0
        else:
            return 0
        
    def write_high_score(self):
        with open(self.FILENAME, "w") as file:
            file.write(f"{self.high_score}")