import os
import re


import xlrd
import copy

from art import *
from Classes.Lab import Lab
from Classes.SchGroup import SchGroup
from Classes.Tutorial import Tutorial
from operator import attrgetter

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tables_path = os.path.join(base_dir, 'tables_excel')
database_files = os.path.join(base_dir, 'Database_files')
file_path = ''
sheet = None
groups = []
course_name = ''
group_number = ''
term_number = ''
day = ''
fr = ''
to = ''
department = ''
line_id = 1


def set_group_number(cell_text):
    global group_number
    if '10' in cell_text:
        group_number = 10
    elif '1' in cell_text:
        group_number = 1
    elif '2' in cell_text:
        group_number = 2
    elif '3' in cell_text:
        group_number = 3
    elif '4' in cell_text:
        group_number = 4
    elif '5' in cell_text:
        group_number = 5
    elif '6' in cell_text:
        group_number = 6
    elif '7' in cell_text:
        group_number = 7
    elif '8' in cell_text:
        group_number = 8
    elif '9' in cell_text:
        group_number = 9
    else:
        return -1


def set_term_number(cell_text):
    global term_number
    if cell_text.startswith('10'):
        term_number = 10
    elif cell_text.startswith('1'):
        term_number = 1
    elif cell_text.startswith('2'):
        term_number = 2
    elif cell_text.startswith('3'):
        term_number = 3
    elif cell_text.startswith('4'):
        term_number = 4
    elif cell_text.startswith('5'):
        term_number = 5
    elif cell_text.startswith('6'):
        term_number = 6
    elif cell_text.startswith('7'):
        term_number = 7
    elif cell_text.startswith('8'):
        term_number = 8
    elif cell_text.startswith('9'):
        term_number = 9
    elif cell_text.startswith('Hu'):
        term_number = 11
    else:
        return -1


def set_day(cell_text):
    global day
    if cell_text.startswith("Sa"):
        day = 0
    elif cell_text.startswith("Su"):
        day = 1
    elif cell_text.startswith("Mo"):
        day = 2
    elif cell_text.startswith("Tu"):
        day = 3
    elif cell_text.startswith("Wed"):
        day = 4
    elif cell_text.startswith("Th"):
        day = 5
    return


def set_from_to(cell_text):
    global fr, to
    if cell_text.startswith("1-") or cell_text.startswith("1 -"):
        fr = 0
        to = 1
        return True
    elif cell_text.startswith("3-") or cell_text.startswith("3 -"):
        fr = 2
        to = 3
        return True
    elif cell_text.startswith("5-") or cell_text.startswith("5 -"):
        fr = 4
        to = 5
        return True
    elif cell_text.startswith("7-") or cell_text.startswith("7 -"):
        fr = 6
        to = 7
        return True
    elif cell_text.startswith("9-") or cell_text.startswith("9 -"):
        fr = 8
        to = 9
        return True
    elif cell_text.startswith("11-") or cell_text.startswith("11 -"):
        fr = 10
        to = 11
        return True
    return False


def set_group(group_courses):
    global course_name
    if course_name not in group_courses:
        group_courses[course_name] = SchGroup(True)
        group_courses[course_name].number = group_number
        group_courses[course_name].courseTerm = term_number
    group = group_courses[course_name]
    group.lecture.courseName = clean_course_name(course_name)
    for i in range(len(group.tutorials)):
        group.tutorials[i].courseName = clean_course_name(course_name)
    for i in range(len(group.labs)):
        group.labs[i].courseName = clean_course_name(course_name)
    return group_courses[course_name]


def check_cell_case(left_up, left_down, right_up, right_down, single_row, last_row, row=None):
    if (single_row and (left_up != '' or right_up != '')) or (last_row and (left_up != '' or right_up != '')):
        return 10
    elif left_up != '' and left_down == '' and right_up == '' and right_down == '' and row != sheet.nrows:
        return 1
    elif left_up != '' and left_down != '' and right_up == '' and right_down == '':
        return 2
    elif left_up != '' and left_down != '' and right_up != '' and right_down != '':
        return 3
    elif left_up == '' and left_down == '' and right_up != '' and right_down != '':
        return 4
    elif left_up == '' and left_down == '' and right_up == '' and right_down != ''\
            and sheet.cell_value(row + 1, 1) == '':
        return 5
    elif left_up == '' and left_down != '' and right_up == '' and right_down == ''\
            and sheet.cell_value(row + 1, 1) == '':
        return 6
    elif left_up != '' and left_down == '' and right_up != '' and right_down != ''\
            and sheet.cell_value(row + 1, 1) == '':
        return 7
    elif left_up != '' and left_down != '' and right_up != '' and right_down == ''\
            and sheet.cell_value(row + 1, 1) == '':
        return 8
    elif left_up == '' and left_down == '' and right_up != '' and right_down == ''\
            and sheet.cell_value(row + 1, 1) == '':
        return 9
    elif left_up != '' and left_down == '' and right_up != '' and right_down == '':
        return 11
    elif left_up != '' and left_down != '' and right_up == '' and right_down != '':
        return 12

    else:
        return -1


def create_lab(group, lab_type, right=False):
    global course_name, group_number, day, fr, to
    for i in range(lab_type):
        lab = Lab()
        lab.courseName = clean_course_name(course_name)
        lab.groupNum = group_number
        lab.instName = 'Unknown'
        lab.periodType = 'Lab'
        lab.place = 'Lab'
        lab.type = lab_type
        lab.time.day = day
        lab.time.fr = fr
        lab.time.to = fr
        if right or i == 1:
            lab.time.fr = to
            lab.time.to = to
        group.add_lab(lab)


def create_tutorial(group, place, tut_type, right=False):
    global course_name, group_number, day, fr, to
    for i in range(tut_type):
        tut = Tutorial()
        tut.courseName = clean_course_name(course_name)
        tut.groupNum = group_number
        tut.instName = 'Unknown'
        tut.periodType = 'Tut'
        tut.place = place
        tut.type = tut_type
        tut.time.day = day
        tut.time.fr = fr
        tut.time.to = fr
        if right or i == 1:
            tut.time.fr = to
            tut.time.to = to
        group.add_tut(tut)


def check_lecture_case(row, col, cell_case=1, single_row=False, last_row=False):
    global course_name
    previous = sheet.cell_value(row - 2, col)
    next_cell = ''
    if not last_row:
        next_cell = sheet.cell_value(row + 2, col)
        if cell_case == 2 or single_row:
            next_cell = sheet.cell_value(row + 1, col)
    if 'lec' in str(previous).lower():
        crs_name = modify_course_name(previous.split('-')[0])
        if crs_name.startswith(course_name):
            return 1
    if 'lec' in str(next_cell).lower():
        crs_name = modify_course_name(next_cell.split('-')[0])
        if crs_name.startswith(course_name):
            return 2
    if (cell_case == 1 and single_row) or (cell_case == 2 and single_row):
        return 4
    return 3


def check_place(cell_text):
    cell_text_content = cell_text.split('-')
    if 'place' in cell_text_content[-1].lower():
        if ':' in cell_text_content[-1]:
            place = cell_text_content[-1].split(':')[-1]
        else:
            place = cell_text_content[-1][cell_text_content[-1].lower().find('place') + 5:]
    else:
        cell_text_content = cell_text.split(':')
        if cell_text_content[0] != cell_text:
            place = cell_text_content[-1]
        elif 'tut' in cell_text.lower() and 'place' not in cell_text.lower():
            place = cell_text[cell_text.lower().find('tut') + 3:]
        else:
            if 'place' not in cell_text.lower():
                place = 'Unknown'
            else:
                place = cell_text[cell_text.lower().find('place') + 5:]
            if 'class' in cell_text.lower():
                place = cell_text[cell_text.lower().find('class'):]
    place = place.replace('-', '')
    place = place.strip()
    if place.isdigit():
        place = 'Class ' + place
    place = re.sub(' +', ' ', place)
    if place == '':
        return 'Unknown'
    return place.strip()


def fix_tutorials(tutorials):
    odd = None
    for tut in tutorials:
        if tut.type == 1:
            if tut.time.fr % 2 != 0:
                odd = True
            else:
                odd = False
            break
    for tut in tutorials:
        if tut.type == 2:
            if odd and tut.time.fr % 2 != 0:
                tutorials.remove(tut)
                break
            elif not odd and tut.time.fr % 2 == 0:
                tutorials.remove(tut)
                break


def add_lecture_extension(group, place, case=False):
    group.lecExPlace = place
    group.lecExDay = day
    group.lecExFrom = fr
    if case:
        group.lecExFrom = to
    group.lecExTo = to


def add_lecture(group, row, col, case=False, place=None, inst_down=False):
    global course_name, group_number, day, fr, to
    length = len(course_name)
    main_lecture = sheet.cell_value(row, col)
    lecture = group.lecture
    if inst_down:
        # this case if inst name in left_down and all info in left_up
        lecture.instName = main_lecture[main_lecture.lower().find('dr'):]
    else:
        lecture.instName = main_lecture[main_lecture.lower().find('dr', length + 1):]
    if lecture.instName.strip() == '' or len(lecture.instName) == 1 or lecture.instName.lower() == 'dr':
        lecture.instName = 'Unknown'
    else:
        if lecture.instName.startswith('dr'):
            lecture.instName = lecture.instName.replace('dr', 'Dr ')
        lecture.instName = lecture.instName.replace('.', ' ')
        lecture.instName = lecture.instName.replace('Dr', 'Dr ')
        lecture.instName = lecture.instName.replace('Prof', '')
        lecture.instName = lecture.instName.replace('prof', '')
        lecture.instName = lecture.instName.replace('\n', ' ')
        lecture.instName = lecture.instName.replace(')', ' ')
        lecture.instName = lecture.instName.replace('(', ' ')
        lecture.instName = re.sub(' +', ' ', lecture.instName)
        lecture.instName = lecture.instName.strip()
    if place is not None:
        lecture.place = place
    else:
        lecture.place = check_place(sheet.cell_value(row + 1, col))
    lecture.courseName = clean_course_name(course_name)
    lecture.groupNum = group_number
    lecture.type = 1
    lecture.periodType = 'Lecture'
    lecture.time.day = day
    if case:
        lecture.time.fr = fr
        lecture.time.to = to
    else:
        lecture.time.fr = to
        set_from_to(sheet.cell_value(row, 1))
        lecture.time.to = to
    return row


def write_file():
    global file_path, line_id
    empty = ",,,,,,,"
    f = open(file_path, 'w')
    for group in groups:
        if group.line_id is None:
            group.line_id = line_id
            line_id += 1
        f.write('{},{},{},{},'.format(group.line_id, group.courseTerm, group.creditHours, group.number))
        f.write('{},{},{},{},{},{},{},{},{},{},{},{},'.format(group.lecture.instName, group.lecture.courseName,
                                                              group.lecture.place, group.lecture.type,
                                                              group.lecture.time.day, group.lecture.time.fr,
                                                              group.lecture.time.to, group.lecExPlace, group.lecExDay,
                                                              group.lecExFrom, group.lecExTo,
                                                              group.lecture.periodType))
        if len(group.tutorials) == 0:
            f.write(empty + ",")
            f.write(empty + ",")
        elif len(group.tutorials) == 1:
            f.write(
                '{},{},{},{},{},{},{},{},'.format(group.tutorials[0].instName, group.tutorials[0].courseName,
                                                  group.tutorials[0].place, group.tutorials[0].type,
                                                  group.tutorials[0].time.day, group.tutorials[0].time.fr,
                                                  group.tutorials[0].time.to, group.tutorials[0].periodType))
            f.write(empty + ",")
        else:
            for j in range(2):
                f.write('{},{},{},{},{},{},{},{},'.format(group.tutorials[j].instName,
                                                          group.tutorials[j].courseName,
                                                          group.tutorials[j].place, group.tutorials[0].type,
                                                          group.tutorials[j].time.day,
                                                          group.tutorials[j].time.fr,
                                                          group.tutorials[j].time.to,
                                                          group.tutorials[j].periodType))
        if len(group.labs) == 0:
            f.write(empty + ",")
            f.write(empty + ',' + department + "\n")
        elif len(group.labs) == 1:
            f.write(
                '{},{},{},{},{},{},{},{},'.format(group.labs[0].instName, group.labs[0].courseName,
                                                  group.labs[0].place, group.labs[0].type,
                                                  group.labs[0].time.day, group.labs[0].time.fr,
                                                  group.labs[0].time.to, group.labs[0].periodType))
            f.write(empty + ',' + department + "\n")
        else:
            for j in range(2):
                if j == 0:
                    end = ","
                else:
                    end = ',' + department + "\n"
                f.write('{},{},{},{},{},{},{},{}{}'.format(group.labs[j].instName,
                                                           group.labs[j].courseName,
                                                           group.labs[j].place, group.labs[0].type,
                                                           group.labs[j].time.day,
                                                           group.labs[j].time.fr,
                                                           group.labs[j].time.to,
                                                           group.labs[j].periodType, end))
    f.close()


def extract_table():
    global group_number, term_number, course_name, day, fr, to, sheet
    col = 2
    start_row = 0
    group_courses = {}  # courses in the same group (vertically) in the table
    while not sheet.cell_value(start_row, col).startswith('G'):
        start_row += 1
        if start_row == 5:
            col += 1
            start_row = 0
    temp_col = col
    while set_term_number(sheet.cell_value(start_row - 1, temp_col)) == -1:
        temp_col += 1
        set_term_number(sheet.cell_value(start_row - 1, temp_col))
    # col = 11
    while col < sheet.ncols:
        row = start_row + 1
        while not sheet.cell_value(row, 0).startswith('Sa'):
            row += 1
        set_group_number(sheet.cell_value(start_row, col))
        set_term_number(sheet.cell_value(start_row - 1, col))
        while row < sheet.nrows:
            single_row = False
            last_row = True
            left_up = sheet.cell_value(row, col)
            right_up = sheet.cell_value(row, col + 1)

            left_down = None
            right_down = None
            if row != sheet.nrows - 1:
                last_row = False
                left_down = sheet.cell_value(row + 1, col)
                right_down = sheet.cell_value(row + 1, col + 1)

            if set_group_number(sheet.cell_value(start_row, col + 1)) != -1:
                right_up = ''
                right_down = ''

            left_up = str(left_up); left_down = str(left_down); right_up = str(right_up); right_up = str(right_up)
            cells_group = {'left_up': left_up, 'left_down': left_down, 'right_up': right_up, 'right_down': right_down}
            set_day(sheet.cell_value(row, 0))

            set_from_to(sheet.cell_value(row, 1))
            if not last_row and str(sheet.cell_value(row + 1, 1)) != '':
                single_row = True

            case = check_cell_case(left_up, left_down, right_up, right_down, single_row, last_row, row)
            if case == -1:
                row += 1
                continue

            course_name = extract_course_name(left_up, left_down, right_up, right_down, case)
            length_1 = len(course_name)
            course_name = modify_course_name(course_name)
            length_2 = len(course_name)
            length = min(length_1, length_2)
            if course_name == '':
                row += 1
                continue
            group = None
            if not course_name.lower().startswith('place'):
                group = set_group(group_courses)

            cases_execution = manage_cases(case, group, row, col, group_courses, length, single_row, cells_group, start_row, last_row)
            if cases_execution is not None:
                # continue case
                if cases_execution > 1000:
                    row = cases_execution - 1000
                    continue
                else:
                    row = cases_execution

            if not last_row and sheet.cell_value(row + 1, 1) != '':
                row += 1
            else:
                row += 1
                if row != sheet.nrows:
                    set_day(sheet.cell_value(row, 0))
                row += 1

        col += 1
        if set_term_number(sheet.cell_value(1, col)) == -1:
            col += 1

        group_courses = fix_groups(group_courses)
        fill_credit_hours(group_courses.values())
        for group in group_courses.values():
            groups.append(group)
        group_courses.clear()
        write_file()
    groups.clear()


def set_department(file):
    global department
    if file.lower().startswith('cce'):
        department = 'CCE'
    elif file.lower().startswith('eme'):
        department = 'EME'
    elif file.lower().startswith('general'):
        department = 'General'
    elif file.lower().startswith('gpe'):
        department = 'GPE'
    elif file.lower().startswith('oce'):
        department = 'OCE'
    else:
        department = 'None'


def fill_credit_hours(group_courses):
    credit_hours = {'h rights': 1, 'human rights': 1, 'history of engineering': 1, 'english language': 2, 'technical writing': 2,
                    'economics': 2, 'project management': 2, 'ethics': 2, 'human resource management': 2,
                    'accounting': 2, 'strategic management': 2, 'computer and society': 2, 'marketing': 2,
                    'finance': 2, 'human computer interaction': 2, 'feasibility': 2, 'analytical skills': 2,
                    'communication laws': 2, 'construction contracts and law': 2, 'communication skills': 2,
                    'principles of industrial health': 2, 'social risks of computer systems': 2,
                    'programming 2': 4, 'computer networks': 4, 'database': 4, 'project 2': 4}

    for group in group_courses:
        for item in credit_hours:
            if group.lecture.courseName.lower().startswith(item) or item.startswith(group.lecture.courseName.lower()):
                group.creditHours = credit_hours[item]
        if group.creditHours is None:
            if term_number == 11:
                group.creditHours = 2
            else:
                group.creditHours = 3


def find_words(start, target_text, cell_text):
    if cell_text.find(target_text, start) != -1:
        return True
    return False


def extract_course_name(left_up, left_down, right_up, right_down, case):
    if case == 4 or case == 9:
        return right_up.split('-')[0]
    elif case == 5:
        return right_down.split('-')[0]
    elif case == 6:
        return left_down.split('-')[0]
    elif case == 10:
        if left_up != '':
            return left_up.split('-')[0]
        else:
            return right_up.split('-')[0]
    else:
        return left_up.split('-')[0]


def manage_cases(case, group, row, col, group_courses, length, single_row, cells_group, start_row, last_row):
    if case == 1:
        return execute_case_1(group, row, col, length, start_row, single_row, cells_group)
    elif case == 2:
        return execute_case_2(group, row, col, group_courses, length, single_row, start_row, cells_group)
    elif case == 3:
        execute_case_3(group, group_courses, length, cells_group)
    elif case == 4:
        execute_case_4(group, length, cells_group)
    elif case == 5:
        execute_case_5(group, length, cells_group, row, col)
    elif case == 6:
        return execute_case_6(group, row, col, length, cells_group)
    elif case == 7:
        execute_case_7(group, group_courses, length, cells_group)
    elif case == 8:
        execute_case_8(group, group_courses, length, cells_group)
    elif case == 9:
        execute_case_9(group, length, cells_group)
    elif case == 10:
        return execute_case_10(group, row, col, group_courses, length, cells_group, start_row, last_row)
    elif case == 11:
        execute_case_11(group, row, col, group_courses, length, cells_group, start_row, last_row)
    elif case == 12:
        execute_case_12(group, row, col, group_courses, length, cells_group, start_row, last_row)


def is_in_merged_cells(row, col):
    merged_cells = sheet.merged_cells
    for cell in merged_cells:
        rlo, rhi, clo, chi = cell
        if rlo <= row < rhi and clo <= col < chi:
            if chi - col == 2:
                return 'long_cell'
            elif chi - col == 1:
                return 'short_cell'
    return False


def execute_case_1(group, row, col, length, start_row, single_row, cells_group):
    left_up = cells_group['left_up']

    if find_words(length, 'lec', left_up.lower()):
        # special case of skipping one row after lecture info and have place in the row after
        if row != sheet.nrows - 2 and sheet.cell_value(row + 2, col).lower().startswith('place'):
            place = check_place(sheet.cell_value(row + 2, col))
            add_lecture(group, row, col, True, place)
            row += 2
            return row
        # special cases of project 1 and project 2
        if course_name.lower() == 'project 1' or course_name.lower() == 'project 2' or course_name.lower() == 'project1' \
                or course_name.lower() == 'project2':
            single_row = True
        lecture_case = check_lecture_case(row, col, 1, single_row)
        if lecture_case == 1:
            group.lecture.time.to = fr
        elif lecture_case == 2:
            if single_row:
                row += 1
            else:
                row += 2
            add_lecture(group, row, col)
        elif lecture_case == 3:
            place = check_place(left_up)
            add_lecture_extension(group, place)
        elif lecture_case == 4:
            place = check_place(left_up)
            add_lecture(group, row, col, True, place)
    elif find_words(length, 'tut', left_up.lower()):
        # special case of skipping one row after tutorial info and have place in the row after
        if row != sheet.nrows - 2 and sheet.cell_value(row + 1, col) == '' and sheet.cell_value(row + 2, col).lower().startswith('place'):
            place = check_place(sheet.cell_value(row + 2, col))
            row += 2
            create_tutorial(group, place, 1)
        else:
            place = check_place(left_up)
            create_tutorial(group, place, 1)
            if is_in_merged_cells(row, col) == 'long_cell':
                group.tut_wait = True
            elif is_in_merged_cells(row, col) == 'short_cell' and sheet.cell_value(start_row - 1, col + 1) != '':
                group.tut_wait = True
            else:
                group.tut_case = 1
    elif find_words(length, 'lab', left_up.lower()):
        create_lab(group, 2)
        if is_in_merged_cells(row, col) == 'short_cell':
            group.labs.remove(group.labs[-1])
            group.lab_case = 1
        elif not is_in_merged_cells(row, col):
            group.labs[0].type = 1
            group.labs.remove(group.labs[-1])
            group.lab_wait = True
    return row


def execute_case_2(group, row, col, group_courses, length, single_row, start_row, cells_group):
    global course_name, sheet
    left_up = cells_group['left_up']; left_down = cells_group['left_down']

    exp_length = 0
    if left_down.split('-')[0] != left_down:
        len_1 = len(left_down.split('-')[0])
        expected_course_name = modify_course_name(left_down.split('-')[0])
        exp_length = min(len_1, len(expected_course_name))

    cell_case = is_in_merged_cells(row, col)
    # if not course_name.lower().startswith('place'):
    if not find_words(length, 'lec', left_up.lower()) and not find_words(exp_length, 'lec', left_down.lower()):
        # the second part of condition because there is a case not containing tut word but its actually tutorial
        # so the differentiation with place word
        if find_words(length, 'tut', left_up.lower()):  #  or find_words(0, 'place', left_down.lower())
            if find_words(exp_length, 'place', left_down.lower()) and not find_words(exp_length, 'tut', left_down.lower()) \
                    and not find_words(exp_length, 'lab', left_down.lower()):
                place = check_place(left_down)
                create_tutorial(group, place, 1)
                if cell_case == 'long_cell':
                    group.tut_wait = True
                elif sheet.cell_value(start_row - 1, col + 1) != '':
                    group.tut_wait = True
                row += 2
                return row + 1000
            else:
                place = check_place(left_up)
                create_tutorial(group, place, 2)
        elif find_words(length, 'lab', left_up.lower()):
            if find_words(exp_length, 'place', left_down.lower()) and not find_words(exp_length, 'tut',
                                                                                     left_down.lower()) \
                    and not find_words(exp_length, 'lab', left_down.lower()):
                create_lab(group, 1)
                row += 2
                return row + 1000
            else:
                create_lab(group, 1)
                group.lab_wait = True
        elif not find_words(length, 'lab', left_up.lower()) and find_words(length, 'lab', left_down.lower()):
            create_lab(group, 2)
        else:
            if find_words(length, 'Dr', left_up):
                if left_down.lower().startswith('place'):
                    place = check_place(left_down)
                    add_lecture(group, row, col, True, place)
                    row += 2
                    return row + 1000
            elif find_words(0, 'place', left_down.lower()):
                place = check_place(left_down)
                create_tutorial(group, place, 1)
                # group.tut_wait = True
                row += 2
                return row + 1000
        course_name = left_down.split('-')[0]
        course_name = modify_course_name(course_name)
        if course_name == '':
            return row
        group = set_group(group_courses)

        if find_words(exp_length, 'tut', left_down.lower()):
            place = check_place(left_down)
            create_tutorial(group, place, 2)
        elif find_words(exp_length, 'lab', left_down.lower()):
            create_lab(group, 2)

    elif find_words(length, 'lec', left_up.lower()) and not find_words(exp_length, 'lec', left_down.lower()):
        half = False
        if course_name.lower() == 'project 1' or course_name.lower() == 'project 2' or course_name.lower() == 'project1'\
                or course_name.lower() == 'project2':
            single_row = True
        if left_down.startswith('Place'):
            add_lecture(group, row, col, True)
            return row
        # this case if all information of lecture was written in left_up cell and left_down has the inst name only
        elif 'place' in left_up[length:].lower() and 'Dr' in left_down:
            place = check_place(left_up)
            add_lecture(group, row + 1, col, True, place, True)
            return
        elif check_lecture_case(row, col, 1, single_row) == 1:
            group.lecture.time.to = fr
            half = True
        elif check_lecture_case(row, col, 1, single_row) == 3:
            place = check_place(left_up)
            add_lecture_extension(group, place)
        elif check_lecture_case(row, col, 1, single_row) == 4:
            place = check_place(left_up)
            add_lecture(group, row, col, True, place)

        course_name = left_down.split('-')[0]
        course_name = modify_course_name(course_name)
        if course_name == '':
            return row
        group = set_group(group_courses)

        if find_words(exp_length, 'tut', left_down.lower()):
            place = check_place(left_down)
            # for case of completion of lecture and tut after it
            if half:
                create_tutorial(group, place, 1, True)
            else:
                create_tutorial(group, place, 2)
            if len(group.tutorials) > 2:
                fix_tutorials(group.tutorials)
        elif find_words(exp_length, 'lab', left_down.lower()):
            if len(group.labs) > 0:
                create_lab(group, 1, True)
            else:
                create_lab(group, 2)
            group.lab_case = 2
        else:
            place = 'Unknown'
            create_tutorial(group, place, 1)
            # if half:

    elif not find_words(length, 'lec', left_up.lower()) and find_words(exp_length, 'lec', left_down.lower()):
        if not single_row:
            if find_words(length, 'tut', left_up.lower()):
                place = check_place(left_up)
                create_tutorial(group, place, 2)
            elif find_words(length, 'lab', left_up.lower()):
                create_lab(group, 2)
                group.lab_case = 2
            lecture_case = check_lecture_case(row + 1, col, 2)
            if lecture_case == 2:
                row += 2
                add_lecture(group, row, col)
            elif lecture_case == 3:
                place = check_place(left_down)
                add_lecture_extension(group, place)
        else:
            if find_words(length, 'tut', left_up.lower()):
                place = check_place(left_up)
                create_tutorial(group, place, 2)
            elif find_words(length, 'lab', left_up.lower()):
                create_lab(group, 2)
                group.lab_case = 2

    elif find_words(length, 'lec', left_up.lower()) and find_words(exp_length, 'lec', left_down.lower()):
        if not single_row:
            if group.lecture.instName == '':
                add_lecture(group, row, col, True)
            else:
                lecture_case = check_lecture_case(row, col)
                if lecture_case == 1:
                    group.lecture.time.to = fr
                elif lecture_case == 3:
                    place = check_place(left_up)
                    add_lecture_extension(group, place)
            course_name = modify_course_name(left_down.split('-')[0])
            group = set_group(group_courses)
            lecture_case = check_lecture_case(row + 1, col, 2)
            if lecture_case == 2:
                row += 2
                add_lecture(group, row, col)
            elif lecture_case == 3:
                if sheet.cell_value(row + 2, col).lower().startswith('place'):
                    if group.lecture.instName != '':
                        place = check_place(sheet.cell_value(row + 2, col))
                        set_from_to(sheet.cell_value(row + 2, 1))
                        group.lecture.place = place
                        group.lecture.time.to = fr
                else:
                    place = check_place(left_down)
                    add_lecture_extension(group, place, True)
        else:
            lecture_case = check_lecture_case(row, col, 1, single_row)
            if lecture_case == 1:
                group.lecture.time.to = fr
            elif lecture_case == 2:
                row += 1
                add_lecture(group, row, col)
            elif lecture_case == 3:
                place = check_place(left_up)
                add_lecture_extension(group, place)
    return row


def execute_case_3(group, group_courses, length, cells_group):
    global course_name
    left_up = cells_group['left_up']; left_down = cells_group['left_down']
    right_up = cells_group['right_up']; right_down = cells_group['right_down']

    exp_length = 0
    if right_up.split('-')[0] != right_up:
        len_1 = len(right_up.split('-')[0])
        expected_course_name = modify_course_name(right_up.split('-')[0])
        exp_length = min(len_1, len(expected_course_name))

    if not left_down.split('-')[0].lower().startswith('place'):
        if find_words(length, 'tut', left_up.lower()):
            place = check_place(left_up)
            create_tutorial(group, place, 1)
        elif find_words(length, 'lab', left_up.lower()):
            create_lab(group, 1)
        course_name = left_down.split('-')[0]
        course_name = modify_course_name(course_name)
        group = set_group(group_courses)
        if find_words(length, 'tut', left_down.lower()):
            place = check_place(left_down)
            create_tutorial(group, place, 1)
        elif find_words(length, 'lab', left_down.lower()):
            create_lab(group, 1)
    else:
        if find_words(length, 'tut', left_up.lower()):
            place = check_place(left_down)
            create_tutorial(group, place, 1)
        elif find_words(length, 'lab', left_up.lower()):
            create_lab(group, 1)

    course_name = right_up.split('-')[0]
    course_name = modify_course_name(course_name)
    group = set_group(group_courses)

    if not right_down.split('-')[0].lower().startswith('place'):
        if find_words(exp_length, 'tut', right_up.lower()):
            place = check_place(right_up)
            create_tutorial(group, place, 1, True)
        elif find_words(exp_length, 'lab', right_up.lower()):
            create_lab(group, 1, True)
        course_name = right_down.split('-')[0]
        course_name = modify_course_name(course_name)
        group = set_group(group_courses)
        if find_words(exp_length, 'tut', right_down.lower()):
            place = check_place(right_down)
            create_tutorial(group, place, 1, True)
        elif find_words(exp_length, 'lab', right_down.lower()):
            create_lab(group, 1, True)
    else:
        if find_words(exp_length, 'tut', right_up.lower()):
            place = check_place(right_down)
            create_tutorial(group, place, 1, True)
        elif find_words(exp_length, 'lab', right_up.lower()):
            create_lab(group, 1, True)


def execute_case_4(group, length, cells_group):
    right_up = cells_group['right_up']; right_down = cells_group['right_down']

    # the second part of condition because there is a case not containing tut word but its actually tutorial
    # so the differentiation with place word
    if find_words(length, 'tut', right_up.lower()):
        place = check_place(right_down)
        create_tutorial(group, place, 1, True)
    elif find_words(length, 'lab', right_up.lower()):
        create_lab(group, 1, True)
    else:
        place = check_place(right_down)
        create_tutorial(group, place, 1, True)


def execute_case_5(group, length, cells_group, row, col):
    global sheet
    right_down = cells_group['right_down']
    if sheet.cell_value(row + 2, col + 1) == '' and sheet.cell_value(row + 3, col + 1).lower().startswith('place'):
        set_from_to(sheet.cell_value(row + 2, 1))
        if find_words(length, 'tut', right_down.lower()):
            place = check_place(sheet.cell_value(row + 3, col + 1))
            create_tutorial(group, place, 1, True)
        elif find_words(length, 'lab', right_down.lower()):
            create_lab(group, 1, True)
    else:
        if find_words(length, 'tut', right_down.lower()):
            place = check_place(right_down)
            create_tutorial(group, place, 1, True)
        elif find_words(length, 'lab', right_down.lower()):
            create_lab(group, 1, True)


def execute_case_6(group, row, col, length, cells_group):
    global sheet
    left_down = cells_group['left_down']

    if sheet.cell_value(row + 1, 1) == '':
        if not find_words(length, 'tut', left_down.lower()) and not find_words(length, 'lab', left_down.lower()) and\
                sheet.cell_value(row + 2, col).lower().startswith('place'):
            set_from_to(sheet.cell_value(row + 3, 1))
            place = check_place(sheet.cell_value(row + 2, col))
            add_lecture(group, row + 1, col, False, place)
            row += 3
            return row + 1000
        elif find_words(length, 'tut', left_down.lower()):
            place = check_place(left_down)
            create_tutorial(group, place, 1, True)
        elif find_words(length, 'lab', left_down.lower()):
            # special cases of project 1 and project 2
            if course_name == 'Project 1' or 'Project 2':
                create_lab(group, 2)
                group.lab_case = 6
            else:
                create_lab(group, 1, True)
        else:
            if group.lecture.groupNum != '':
                place = check_place(left_down)
                add_lecture_extension(group, place)


def execute_case_7(group, group_courses, length, cells_group):
    global course_name
    left_up = cells_group['left_up']; right_up = cells_group['right_up']; right_down = cells_group['right_down']

    exp_length = 0
    if right_up.split('-')[0] != right_up:
        len_1 = len(right_up.split('-')[0])
        expected_course_name = modify_course_name(right_up.split('-')[0])
        exp_length = min(len_1, len(expected_course_name))

    if find_words(length, 'lab', left_up.lower()):
        create_lab(group, 1)
    elif find_words(length, 'tut', left_up.lower()):
        place = check_place(left_up)
        create_tutorial(group, place, 1)

    course_name = right_up.split('-')[0]
    course_name = modify_course_name(course_name)
    group = set_group(group_courses)

    if find_words(exp_length, 'lab', right_up.lower()):
        create_lab(group, 1, True)
    else:
        place = check_place(right_down)
        create_tutorial(group, place, 1, True)


def execute_case_8(group, group_courses, length, cells_group):
    global course_name
    left_up = cells_group['left_up']; left_down = cells_group['left_down']
    right_up = cells_group['right_up']

    exp_length = 0
    if right_up.split('-')[0] != right_up:
        len_1 = len(right_up.split('-')[0])
        expected_course_name = modify_course_name(right_up.split('-')[0])
        exp_length = min(len_1, len(expected_course_name))

    if find_words(length, 'lab', left_up.lower()):
        create_lab(group, 1)
    else:
        place = check_place(left_down)
        create_tutorial(group, place, 1)

    course_name = right_up.split('-')[0]
    course_name = modify_course_name(course_name)
    group = set_group(group_courses)

    if find_words(exp_length, 'tut', right_up.lower()):
        place = check_place(right_up)
        create_tutorial(group, place, 1, True)
    elif find_words(exp_length, 'lab', right_up.lower()):
        create_lab(group, 1, True)


def execute_case_9(group, length, cells_group):
    right_up = cells_group['right_up']

    if find_words(length, 'tut', right_up.lower()):
        place = check_place(right_up)
        create_tutorial(group, place, 1, True)
    elif find_words(length, 'lab', right_up.lower()):
        create_lab(group, 1, True)
    else:
        place = 'Unknown'
        create_tutorial(group, place, 1, True)


def execute_case_10(group, row, col, group_courses, length, cells_group, start_row, last_row):
    global course_name, sheet
    left_up = cells_group['left_up']; right_up = cells_group['right_up']

    case = 0
    if left_up != '' and right_up != '':
        case = 2
    elif left_up == '' and right_up != '':
        case = 3

    cell_case = is_in_merged_cells(row, col)

    if left_up != '':
        if find_words(length, 'lab', left_up.lower()):
            create_lab(group, 1)
            if cell_case == 'long_cell':
                group.lab_wait = True
            elif sheet.cell_value(start_row - 1, col + 1) != '':
                group.lab_wait = True
        elif find_words(length, 'tut', left_up.lower()):
            place = check_place(left_up)
            create_tutorial(group, place, 1)
            if cell_case == 'long_cell':
                group.tut_wait = True
            elif sheet.cell_value(start_row - 1, col + 1) != '':
                group.tut_wait = True
        elif find_words(length, 'lec', left_up.lower()):
            lecture_case = check_lecture_case(row, col, 1, True, last_row)
            if lecture_case == 1:
                group.lecture.time.to = fr
            elif lecture_case == 2:
                place = check_place(sheet.cell_value(row + 1, col))
                # row += 1
                add_lecture(group, row, col, False, place)
            elif lecture_case == 3:
                place = check_place(left_up)
                add_lecture_extension(group, place)
            elif lecture_case == 4:
                if sheet.cell_value(row + 1, col).lower().startswith('place'):
                    place = check_place(sheet.cell_value(row + 1, col))
                else:
                    place = check_place(left_up)
                add_lecture(group, row, col, True, place)
    if case == 2 or case == 3:
        course_name = right_up.split('-')[0]
        course_name = modify_course_name(course_name)
        length = len(course_name)
        if course_name == '':
            return row
        group = set_group(group_courses)

        if find_words(length, 'lab', right_up.lower()):
            create_lab(group, 1, True)
        elif find_words(length, 'tut', right_up.lower()):
            place = check_place(right_up)
            create_tutorial(group, place, 1, True)
        # elif find_words(length, 'lec', right_up.lower()):
        #     lecture_case = check_lecture_case(row, col, 1, True)
        #     if lecture_case == 1:
        #         group.lecture.time.to = fr
        #     elif lecture_case == 2:
        #         row += 1
        #         add_lecture(group, row, col)
        #     elif lecture_case == 3:
        #         place = check_place(right_up)
        #         add_lecture_extension(group, place)
        #     elif lecture_case == 4:
        #         place = check_place(right_up)
        #         add_lecture(group, row, col, True, place)
    return row


def execute_case_11(group, row, col, group_courses, length, cells_group, start_row, last_row):
    global course_name
    left_up = cells_group['left_up']; right_up = cells_group['right_up']
    if find_words(length, 'tut', left_up.lower()):
        place = check_place(left_up)
        create_tutorial(group, place, 1)
    elif find_words(length, 'lab', left_up.lower()):
        create_lab(group, 1)

    course_name = right_up.split('-')[0]
    course_name = modify_course_name(course_name)
    length = len(course_name)
    if course_name == '':
        return
    group = set_group(group_courses)

    if find_words(length, 'tut', right_up.lower()):
        place = check_place(right_up)
        create_tutorial(group, place, 1, True)
    elif find_words(length, 'lab', right_up.lower()):
        create_lab(group, 1, True)


def execute_case_12(group, row, col, group_courses, length, cells_group, start_row, last_row):
    left_up = cells_group['left_up']; left_down = cells_group['left_down']; right_down = cells_group['right_down']
    if right_down.lower().startswith('place'):
        if left_down.lower().startswith('place'):
            if find_words(length, 'tut', left_up.lower()):
                place = check_place(left_down)
                create_tutorial(group, place, 1)
            elif find_words(length, 'lab', left_up.lower()):
                create_lab(group, 1)


def modify_course_name(name):
    saved_names = {'Prog': 'Programming', 'Phy': 'Physics', 'Thermo': 'Thermodynamics'}
    for saved_name in saved_names:
        if saved_name == name[:len(saved_name)] and len(name[len(saved_name):]) <= 3:
            name = name.replace(saved_name, saved_names[saved_name])

    name = name.strip()
    name = name.replace('.', '')
    name = name.replace(':', '')

    if name.find('(') != -1 and name.find(')') != -1:
        index = name.find(')')
        name = name[:index + 1]

    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.rstrip(' ')

    # for ProjectLec in term 10
    if name.lower().endswith('lec'):
        name = name[:len(name) - 3]
    elif name.lower().endswith('tut'):
        name = name[:len(name) - 3]
    elif name.lower().endswith('lab'):
        name = name[:len(name) - 3]

    name = name.rstrip(' ')
    if name.lower() == 'place':
        name = ''

    if name.endswith('IV'):
        name = name.rstrip('IV')
        name = name + '4'
    elif name.endswith('III'):
        name = name.rstrip('III')
        name = name + '3'
    elif name.endswith('II'):
        name = name.rstrip('II')
        name = name + '2'
    # special case of lI
    elif name.endswith('lI'):
        name = name.rstrip('lI')
        name = name + '2'
    elif name.endswith('I'):
        name = name.rstrip('I')
        name = name + '1'
    elif name.endswith('l') and name[-2] == ' ':
        name = name.rstrip('l')
        name = name + '1'

    name = re.sub(' +', ' ', name)
    name = name.rstrip(' ')
    return name


def clean_course_name(name):
    if name[-2] != ' ' and name[-1].isdigit():
        name = name[:-1] + ' ' + name[-1]
    return name


def check_common_words(name1, name2, times):
    name1 = clean_course_name(name1)
    name2 = clean_course_name(name2)

    name1_words = name1.split(' ')
    name2_words = name2.split(' ')

    counter = 0
    digits = 0
    # repeated words that makes comparison not accurate
    rejected_words = ['and', 'or', 'of', 'to', 'introduction', 'marine']
    for word in name1_words:
        for word2 in name2_words:
            if (word.lower() == word2.lower() or word.lower()[:-1] == word2.lower()) and word.lower() not in rejected_words:
                if word.isdigit():
                    digits += 1
                counter += 1
                break
    if counter == 1:
        if digits == 1:
            return 'no'
        return 'continue' if times == 1 else 'yes'
    else:
        return 'yes' if counter >= 2 else 'no'


def empty_lecture(group):
    return group.lecture.place == ''


def empty_tutorials(group):
    return len(group.tutorials) == 0


def empty_labs(group):
    return len(group.labs) == 0


def check_group_case(group):
    if empty_lecture(group) and empty_tutorials(group) and empty_labs(group):
        return 1
    elif empty_lecture(group) and not empty_tutorials(group) and empty_labs(group):
        return 2
    elif empty_lecture(group) and empty_tutorials(group) and not empty_labs(group):
        return 3
    elif empty_lecture(group) and not empty_tutorials(group) and not empty_labs(group):
        return 4
    elif not empty_lecture(group) and empty_tutorials(group) and empty_labs(group):
        return 5
    elif not empty_lecture(group) and not empty_tutorials(group) and empty_labs(group):
        return 6
    elif not empty_lecture(group) and empty_tutorials(group) and not empty_labs(group):
        return 7
    elif not empty_lecture(group) and not empty_tutorials(group) and not empty_labs(group):
        return 8


def can_be_merged(group_1, group_2, times):
    check = check_common_words(group_1.lecture.courseName, group_2.lecture.courseName, times)
    if check_group_case(group_1) == 5 and check_group_case(group_2) == 4\
            and not in_lec_courses(group_1):
        return check
    elif check_group_case(group_1) == 5 and check_group_case(group_2) == 2\
            and not in_lec_courses(group_1):
        return check
    elif check_group_case(group_1) == 5 and check_group_case(group_2) == 3\
            and not in_lec_courses(group_1):
        return check
    elif check_group_case(group_1) == 5 and check_group_case(group_2) == 6\
            and not in_lec_courses(group_1):
        return 'lec_found' if check == 'yes' else check
    elif check_group_case(group_1) == 5 and check_group_case(group_2) == 7\
            and not in_lec_courses(group_1):
        return 'lec_found' if check == 'yes' else check
    elif check_group_case(group_1) == 5 and check_group_case(group_2) == 8\
            and not in_lec_courses(group_1):
        return 'lec_found' if check == 'yes' else check
    elif check_group_case(group_1) == 6 and check_group_case(group_2) == 3:
        return check
    elif check_group_case(group_1) == 7 and check_group_case(group_2) == 2:
        return check
    return 'no'


def merge_groups(group_1, group_2, case=0):
    if len(group_1.tutorials) < 2:
        group_1.tutorials = group_2.tutorials
    if len(group_1.labs) < 2:
        group_1.labs = group_2.labs
    if case == 1:
        merge_lecture_information(group_1, group_2)


def merge_lecture_information(group_1, group_2):
    lecture_1 = group_1.lecture
    lecture_2 = group_2.lecture

    # lecture completion
    if lecture_2.time.fr - lecture_1.time.fr == 2:
        lecture_1.time.to = lecture_2.time.fr
    elif lecture_1.time.fr - lecture_2.time.fr == 2:
        lecture_1.time.fr = lecture_2.time.to

    # lecture extension
    elif abs(lecture_1.time.fr - lecture_2.time.fr) != 2:
        group_1.lecExPlace = group_2.lecExPlace
        group_1.lecExDay = group_2.lecExDay
        group_1.lecExFrom = group_2.lecExFrom
        group_1.lecExTo = group_2.lecExTo


def fix_waiting_groups(saved_groups):
    for group in saved_groups:
        if group.tut_wait:
            if len(group.tutorials) == 1:
                tut = copy.deepcopy(group.tutorials[0])
                if tut.time.fr == 0 or tut.time.fr % 2 == 0:
                    tut.time.fr += 1
                    tut.time.to += 1
                else:
                    tut.time.fr -= 1
                    tut.time.to -= 1
                group.tutorials[0].type = 2
                tut.type = 2
                group.tutorials.append(tut)
            group.tut_wait = False
        if group.lab_wait:
            if len(group.labs) == 1:
                lab = copy.deepcopy(group.labs[0])
                if lab.time.fr == 0 or lab.time.fr % 2 == 0:
                    lab.time.fr += 1
                    lab.time.to += 1
                else:
                    lab.time.fr -= 1
                    lab.time.to -= 1
                group.labs[0].type = 2
                lab.type = 2
                group.labs.append(lab)

            group.lab_wait = False
        # special case of being tutorial or lab in left part of cell and
        if len(group.tutorials) == 1 and group.tut_case == 1:
            group.tutorials[0].type = 2

        # if len(group.tutorials) == 1 and len(group.labs) == 2 and group.lab_case == 1:
        #     group.labs.remove(group.labs[-1])

        # just if needed
        if len(group.labs) == 2 and group.lab_case == 1:
            group.labs[0].type = 1


def in_lec_courses(group):
    lec_courses = ['History', 'English']
    for name in lec_courses:
        if group.lecture.courseName.startswith(name):
            return True
    return False


def fix_groups(saved_groups):
    all_groups = list(saved_groups.values())
    fix_waiting_groups(all_groups)
    all_groups.sort(key=attrgetter('lecture.instName'), reverse=True)

    for i in range(len(all_groups)):
        test_group = all_groups[i]
        if test_group.lecture.courseName == 'delete':
            continue
        loop = 1
        times = 1
        # continue_check = False
        while loop > 0:
            loop -= 1
            for j in range(i + 1, len(all_groups)):
                group = all_groups[j]
                if group.lecture.courseName == 'delete':
                    continue
                check = can_be_merged(test_group, group, times)
                if test_group != group:
                    if check == 'yes':
                        merge_groups(test_group, group)
                        group.lecture.courseName = 'delete'
                    elif check == 'lec_found':
                        merge_groups(test_group, group, 1)
                        group.lecture.courseName = 'delete'
                    elif check == 'continue':
                        # continue_check = True
                        loop += 1
                        times += 1

            # if continue_check:
            #     loop = 1
            #     continue_check = False

    group_courses = {}
    for key, group in saved_groups.items():
        if group.lecture.courseName != 'delete':
            group_courses[key] = group
    return group_courses


def parse_all_tables():
    global file_path, sheet
    for file in os.listdir(tables_path):
        if file.endswith('.xlsx'):
            wb = xlrd.open_workbook(os.path.join(tables_path, file))
            sheet = wb.sheet_by_index(0)
            file = file.replace('.xlsx', '.csv')
            file_path = os.path.join(database_files, file)
            set_department(file)
            extract_table()


if __name__ == '__main__':
    parse_all_tables()
    # print("Information saved in the files successfully")
    # print("Parsing Done")
    tprint('P a r s i n g                        D o n e')
