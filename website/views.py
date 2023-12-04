from flask import Blueprint, render_template, request, session
import csv
import random
import time

views = Blueprint('views', __name__)
questions = []
point_types = [100,200,300,400,500,600,800,1000,1200,1600]


@views.route('/', methods=['GET'])
def home():
    session.clear()
    return render_template('start.html')

@views.route('/game', methods=['POST'])
def game():
    print(request.form)
    question_index = random.randint(0,18197)
    if 'visited' not in session:
        sort_selected = request.form.get('sort_clicked')
        global questions
        questions = getCSV()
        if sort_selected == 'merge':
            then = time.time()
            merge_sort(questions, 0, len(questions) - 1)
            now = time.time()
            elapsed = now - then
        if sort_selected == 'heap':
            then = time.time()
            heapSort(questions)
            now = time.time()
            elapsed = now - then
        session['visited'] = True
        session['points'] = 0
        question_index = random.randint(0,18197)
        try:
            question = questions[question_index][1]
            answer = questions[question_index][2]
            point_value = questions[question_index][0]
            category = questions[question_index][3]
            session['question'] = [answer, point_value]
            session['index'] = question_index
        except Exception as e:
            question_index = random.randint(210092,256294)
            question = questions[question_index][1]
            answer = questions[question_index][2]
            point_value = questions[question_index][0]
            category = questions[question_index][3]
            session['question'] = [answer, point_value]
            session['index'] = question_index
        print(answer)
        points_total = session['points']
        return render_template('game.html', question=question, answer=answer, point_value=point_value, category=category, points_total=points_total, answered=False, time=True, elapsed=elapsed)
    else:
        if 'submit' in request.form:
            correct = False
            print('checking')
            print(request.form.get('answer-input'))
            if request.form.get('answer-input').lower() == session['question'][0].lower():
                session['points'] += session['question'][1]
                correct = True
            question_index = session['index']
            question = questions[question_index][1]
            answer = questions[question_index][2]
            point_value = questions[question_index][0]
            category = questions[question_index][3]
            session['question'] = [answer, point_value]
            session['index'] = question_index
            

            points_total = session['points']
            return render_template('game.html', question=question, answer=answer, point_value=point_value, category=category, points_total=points_total, answered=True, correct=correct)

        elif 'difficulty' in request.form:
            difficulty = request.form.get('difficulty')
            curDiff = session['question'][1]
            print(curDiff)
            if difficulty == 'hard':
                if curDiff != 1600:
                    nextDiff = point_types.index(curDiff) + 1
                else:
                    nextDiff = point_types.index(curDiff)
            if difficulty == 'easy':
                if curDiff != 100:
                    nextDiff = point_types.index(curDiff) - 1
                else:
                    nextDiff = point_types.index(curDiff)
            nextDiff = point_types[nextDiff]
            if nextDiff == 100:
                question_index = random.randint(0,18197)
            elif nextDiff == 200:
                question_index = random.randint(18197,82911)
            elif nextDiff == 300:
                question_index = random.randint(82911,100690)
            elif nextDiff == 400:
                question_index = random.randint(100690,193049)
            elif nextDiff == 500:
                question_index = random.randint(193049,210092)
            elif nextDiff == 600:
                question_index = random.randint(210092,256294)
            elif nextDiff == 800:
                question_index = random.randint(256294,330593)
            elif nextDiff == 1000:
                question_index = random.randint(330593,375761)
            elif nextDiff == 1200:
                question_index = random.randint(375761,412262)
            elif nextDiff == 1600:
                question_index = random.randint(412262,440572)
            else:
                question_index = random.randint(193049,210092)
    try:
        question = questions[question_index][1]
        answer = questions[question_index][2]
        point_value = questions[question_index][0]
        category = questions[question_index][3]
        session['question'] = [answer, point_value]
        session['index'] = question_index
    except Exception as e:
        question_index = random.randint(210092,256294)
        question = questions[question_index][1]
        answer = questions[question_index][2]
        point_value = questions[question_index][0]
        category = questions[question_index][3]
        session['question'] = [answer, point_value]
        session['index'] = question_index
    print(answer)
    points_total = session['points']
    return render_template('game.html', question=question, answer=answer, point_value=point_value, category=category, points_total=points_total, answered=False)

# 100
#18197 200
#82911 300
#100690 400
#193049 500
#210092 600
#256294 800
#330593 1000
#375761 1200
#412262 1600
#440572
def heapifyDown(array, low, high):
    greatest = high
    left = 2 * high + 1
    right = 2 * high + 2

    if left < low and int(array[greatest][0]) < int(array[left][0]):
        greatest = left

    if right < low and int(array[greatest][0]) < int(array[right][0]):
        greatest = right

    if greatest != high:
        (array[high], array[greatest]) = (array[greatest], array[high])

        heapifyDown(array, low, greatest)


def heapSort(arr):
    n = len(arr)

    # Build a maxheap.
    # Since last parent will be at ((n//2)-1) we can start at that location.

    for i in range(n // 2 - 1, -1, -1):
        heapifyDown(arr, n, i)

    # One by one extract elements

    for i in range(n - 1, 0, -1):
        (arr[i], arr[0]) = (arr[0], arr[i])  # swap
        heapifyDown(arr, i, 0)

def merge(arr, mid_index, left_index, right_index):
    # create a new array from left to mid & mid to right
    n1 = mid_index - left_index + 1
    n2 = right_index - mid_index
    L = [0] * n1
    R = [0] * n2
    for i in range(0, n1):
        L[i] = arr[left_index + i]
    for j in range(0, n2):
        R[j] = arr[mid_index + 1 + j]
    # Merge R and L into into arr
    i = 0
    j = 0
    k = left_index
    while i < n1 and j < n2:
        if int(L[i][0]) <= int(R[j][0]):
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    # When we run out of elements in R or L, append remaining elements
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1
def merge_sort(arr, left_index, right_index):
    if left_index < right_index:
        mid_index = (left_index + right_index) // 2
        merge_sort(arr, left_index, mid_index)
        merge_sort(arr, mid_index + 1, right_index)
        # call merge
        merge(arr, mid_index, left_index, right_index)
def getCSV():
    questions = []

    with open('data.csv', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                #1200 point value assigned to round 3 questions
                if row['round'] == '3':
                    questions.append([1200, row['answer'], row['question']])
                else:
                    questions.append([int(row['clue_value']), row['answer'], row['question'], row['category']])
            except UnicodeEncodeError as e:
                
                print(f"Error storing row: {e}")
        print("done!")

    return questions
  

