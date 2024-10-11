# Read student data from the file
def read_student_data(filename):
    students = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, score = line.strip().split(',')
            students.append((name, int(score)))
    return students

# find average score
def calculate_average(students):
    return sum(score for _, score in students) / len(students)

# find highest and lowest scores
def find_highest_and_lowest(students):
    max_score = max(students, key=lambda x: x[1])[1]
    min_score = min(students, key=lambda x: x[1])[1]
    highest_students = [s for s in students if s[1] == max_score]
    lowest_students = [s for s in students if s[1] == min_score]
    return highest_students, lowest_students

# group students by score
def classify_students(students, avg):
    above_average = [s for s in students if s[1] > avg]
    below_average = [s for s in students if s[1] <= avg]
    return above_average, below_average

# bubble sort
def bubble_sort(students):
    sorted_students = students[:]
    n = len(sorted_students)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sorted_students[j][1] > sorted_students[j + 1][1]:
                sorted_students[j], sorted_students[j + 1] = sorted_students[j + 1], sorted_students[j]
    return sorted_students

# insertion sort
def insertion_sort(students):
    sorted_students = students[:]
    for i in range(1, len(sorted_students)):
        key = sorted_students[i]
        j = i - 1
        while j >= 0 and key[1] < sorted_students[j][1]:
            sorted_students[j + 1] = sorted_students[j]
            j -= 1
        sorted_students[j + 1] = key
    return sorted_students

# linear search
def linear_search(students, target):
    return [s for s in students if s[1] == target]

# binary search
def binary_search_iterative(students, target):
    left, right = 0, len(students) - 1
    results = []
    while left <= right:
        mid = (left + right) // 2
        if students[mid][1] == target:
            i = mid
            while i >= 0 and students[i][1] == target:
                results.append(students[i])
                i -= 1
            i = mid + 1
            while i < len(students) and students[i][1] == target:
                results.append(students[i])
                i += 1
            return results
        elif students[mid][1] < target:
            left = mid + 1
        else:
            right = mid - 1
    return results

# this will write the results to output.txt
def write_results_to_file(filename, avg, highest, lowest, above_avg, below_avg, bubble_sorted, insertion_sorted, linear_results, binary_results):
    with open(filename, 'w') as file:
        file.write(f"Average Score: {avg:.2f}\n\n")

        # highest scores table
        file.write("Students with the Highest Score:\n")
        file.write("Name\tScore\n")
        for s in highest:
            file.write(f"{s[0]}\t{s[1]}\n")
        file.write("\n")

        # lowest scores table
        file.write("Students with the Lowest Score:\n")
        file.write("Name\tScore\n")
        for s in lowest:
            file.write(f"{s[0]}\t{s[1]}\n")
        file.write("\n")

        # above average table
        file.write("Students Scoring Above Average:\n")
        file.write("Name\tScore\n")
        for s in above_avg:
            file.write(f"{s[0]}\t{s[1]}\n")
        file.write("\n")

        # below average table
        file.write("Students Scoring Below Average:\n")
        file.write("Name\tScore\n")
        for s in below_avg:
            file.write(f"{s[0]}\t{s[1]}\n")
        file.write("\n")

        # bubble sorted Table
        file.write("Bubble Sorted Students:\n")
        file.write("Name\tScore\n")
        for s in bubble_sorted:
            file.write(f"{s[0]}\t{s[1]}\n")
        file.write("\n")

        # insertion ordered table
        file.write("Insertion Sorted Students:\n")
        file.write("Name\tScore\n")
        for s in insertion_sorted:
            file.write(f"{s[0]}\t{s[1]}\n")
        file.write("\n")

        # linear search table
        file.write("Linear Search Results:\n")
        file.write("Name\tScore\n")
        if linear_results:
            for s in linear_results:
                file.write(f"{s[0]}\t{s[1]}\n")
        else:
            file.write("No student found with the given score.\n")
        file.write("\n")

        # binary search table
        file.write("Binary Search Results:\n")
        file.write("Name\tScore\n")
        if binary_results:
            for s in binary_results:
                file.write(f"{s[0]}\t{s[1]}\n")
        else:
            file.write("No student found with the given score.\n")

# main work
students = read_student_data("02230309.txt")
average_score = calculate_average(students)
highest_students, lowest_students = find_highest_and_lowest(students)
above_avg_students, below_avg_students = classify_students(students, average_score)
bubble_sorted_students = bubble_sort(students)
insertion_sorted_students = insertion_sort(students)

target_score = int(input("\nEnter the score to search for: "))
linear_search_results = linear_search(students, target_score)
binary_search_results = binary_search_iterative(insertion_sorted_students, target_score)

# write the results to output.txt
write_results_to_file("output.txt", average_score, highest_students, lowest_students,
                      above_avg_students, below_avg_students, bubble_sorted_students,
                      insertion_sorted_students, linear_search_results, binary_search_results)
