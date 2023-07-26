import streamlit as st
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate the L3-norm of a vector
def norm3(vec):
    res = 0
    for el in vec:
        res += pow(el, 3)
    res = res ** (1./3)
    return res

# Generate random student scores
studentList = {}
random.seed(20)
for i in range(225):
    English = random.randint(120, 200)
    Georgian = random.randint(120, 200)
    Math = random.randint(120, 200)
    student = np.array([English, Georgian, Math])
    studentList.update({i: (student, norm3(student))})

# Function to rank students based on their L3-norm scores
def rankStudent():
    return dict(sorted(studentList.items(), key=lambda item: item[1][1]))

# Function to group students into levels
def groupByLevels(rankedStudents):
    studs = list(rankedStudents.values())
    levels = {}
    for i in range(15):
        levels.update({i: []})

    for i in range(15):
        for j in range(15):
            l = levels[i]
            l.append(studs.pop())
            levels.update({i: l})
    return levels

# Backtracking Algorithm to partition students into groups
def backTrace(leveledStudents, avgSum, levelIndex, currSum, currentList):
    # Base case
    if len(currentList) == 15:
        if abs(currSum - avgSum) < 1000:
            return True
        else:
            return False

    List = leveledStudents[levelIndex].copy()
    for index, stud in enumerate(List):
        currSum += stud[1]
        sstud = ((levelIndex, index), stud)
        currentList.append(sstud)

        if currSum > avgSum:
            currSum -= stud[1]
            currentList.remove(sstud)
            return False

        if backTrace(leveledStudents, avgSum, levelIndex + 1, currSum, currentList):
            return True
        else:
            currSum -= stud[1]
            currentList.remove(sstud)
            continue

# Function to partition students into groups
def partition(leveledStudents, avgSum, levelIndex, currSum):
    lStudents = leveledStudents.copy()
    groups = {}
    for i in range(15):
        currentList = []
        backTrace(leveledStudents, avgSum, levelIndex, currSum, currentList)
        groups.update({i: currentList})
        for index, v in enumerate(currentList):
            l = lStudents[14 - index]
            l.pop(v[0][1])
            lStudents[14 - index] = l

    return groups

# Calculate the average score
sum_scores = 0
for k, v in studentList.items():
    sum_scores += v[1]
avgSum = sum_scores / 15.0

# Rank students
ranked_students = rankStudent()

# Group students by levels
leveled_students = groupByLevels(ranked_students)

# Partition students into groups
group = partition(leveled_students, avgSum + 40, 0, 0)
scores = [sum([el[1][1] for el in v]) for k, v in group.items()]

# Streamlit App
st.title("Student Scores Analysis")
st.subheader("Author: Luka Gorgadze")
st.write(
    "This app visualizes and analyzes the scores of a group of students in English, Georgian, and Math subjects."
)

# Display the original student scores as a table
st.header("Original Student Scores")
st.dataframe(pd.DataFrame(studentList).T.rename(columns={0: "Scores", 1: "L3-Norm"}))

# Explanation of L3-Norm
st.markdown(
    r"""
    The L3-Norm of a vector is calculated as follows:
    $$L3-Norm = \left( x_1^3 + x_2^3 + \ldots + x_n^3 \right)^{\frac{1}{3}}$$
    
    It measures the magnitude of a vector with three components (English, Georgian, and Math scores).
    """
)

# Display the grouped student scores as a table
st.header("Grouped Student Scores - Table")
grouped_students_data = {f"Group {i+1}": [stud[1][0] for stud in group[i]] for i in range(15)}
grouped_students_df = pd.DataFrame(grouped_students_data)
st.dataframe(grouped_students_df)

# Display the grouped student scores as a pie chart
st.header("Grouped Student Scores - Pie Chart")
labels = list(group.keys())
sizes = scores
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Explanation of Backtracking Algorithm
st.header("Backtracking Algorithm for Grouping Students")
st.markdown(
    """
    The backtracking algorithm is used to partition the students into 15 groups, aiming to balance their scores
    as closely as possible. It ensures that the sum of scores in each group is as close to the average as possible.
    """
)

# Explanation of the Pie Chart
st.header("Interpreting the Pie Chart")
st.markdown(
    """
    Each slice of the pie chart represents a group of students. The size of the slice indicates the total combined
    score of the students in that group. The goal of the algorithm is to make these slices as equal as possible,
    so the distribution of scores is balanced.
    """
)
