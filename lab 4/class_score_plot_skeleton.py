#이유리22102550
import matplotlib.pyplot as plt
import csv

# Function to read data from a CSV file
def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):  # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data for Korean and English classes
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # Prepare midterm, final, and total scores for the Korean class
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]

    # Prepare midterm, final, and total scores for the English class
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # Plot midterm and final scores as points
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.scatter(midterm_kr, final_kr, c='green', marker='D', label='Korean')
    plt.scatter(midterm_en, final_en, c='blue', marker='+', label='English')
    plt.xlabel('Midterm Scores')
    plt.ylabel('Final Scores')
    plt.legend()

    # Plot total scores as a histogram
    plt.subplot(1, 2, 2)
    plt.hist(total_kr, bins=10, alpha=0.5, color='green', label='Korean')
    plt.hist(total_en, bins=10, alpha=0.5, color='blue', label='English')
    plt.xlabel('Total Scores')
    plt.ylabel('The number of students')
    plt.legend()

    plt.tight_layout()
    plt.show()
