"""
Ashley Ngo
ID:65868419
I don't use external resources.
"""
def read_student_info(filename):
    """this function reads the resume file, store it in memory as a str"""
    with open(filename,'r') as student_info:
        result = []
        lines = student_info.readlines()
        for line in lines:
            line = line.strip('\n')
            result.append(line)
        return result


def detect_name(line):
    line = line.strip()
    if line[0].isupper():
        return line
    else:
        return 'Invalid Name'


def detect_email(lines):
    target_string = ''
    for line in lines:
        if '@' in line:
            target_string = line
    if not target_string:
        return target_string
    target_string = target_string.strip()

    domain = target_string[-4:]
    if domain != ".com" and domain != ".edu":
        return ''
    # check for numbers
    for char in target_string:
        if char.isdigit():
            return ''
    # check for lowercase english char in email
    #BRANDON@upen.edu
    has_lowercase = False
    email_without_domain = target_string.split('@')[0]
    for char in email_without_domain:
        if char.islower():
            has_lowercase = True

    if has_lowercase:
        return target_string

    return ''


def detect_courses(lines):
    target_string = ''
    for line in lines:
        if 'Courses' in line:
            target_string = line
    if not target_string:
        return target_string

    line_start = 0
    target_string = target_string.split('Courses')[1]
    for i in range(len(target_string)):
        if target_string[i].isalpha():
            line_start = i
            break
    courses = target_string[line_start:].split(',')
    result = []
    for course in courses:
        course = course.strip()
        result.append(course)
    return result

def detect_projects(lines):
    starting_line = ''
    ending_line = ''
    for line_number in range(len(lines)):
        line = lines[line_number]
        if 'Projects' in line:
            starting_line = line_number
            break

    for line_number in range(len(lines)):
        line = lines[line_number]
        if '-'*10 in line:
            ending_line = line_number
            break
    if not ending_line or not starting_line:
        return []
    project_lines = lines[starting_line+1:ending_line]
    result = []

    for project in project_lines:
        project = project.strip()
        result.append(project)

    return result

def surround_block(tag, text):
    """
    Surrounds the given text with the given html tag and returns the string.
    """

    # insert code
    block = '<{}>{}</{}>'.format(tag,text,tag)
    return block

def create_email_link(email_address):
    """
    Creates an email link with the given email_address.
    To cut down on spammers harvesting the email address from the webpage,
    displays the email address with [aT] instead of @.

    Example: Given the email address: lbrandon@wharton.upenn.edu
    Generates the email link: <a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>

    Note: If, for some reason the email address does not contain @,
    use the email address as is and don't replace anything.
    """

    # insert code
    #convert email address to spam-proof email address if it contains an at sign
    email_address_prop = email_address.replace("@","[aT]")
    #make a link with tag and href reference to email
    email_link = '<a href="mailto:{}">{}</a>'.format(email_address,email_address_prop)
    return email_link

def read_resume_template(filename):
    with open(filename,'r') as resume_template:
        lines = resume_template.readlines()
        return ''.join(lines[:-2])

def get_resume_content(name, email_address, courses, projects):
    content = []
    # 1st div line
    content.append('<div id="page-wrap">')
    # basic information
    name_line = surround_block('h1', name)
    email_link = create_email_link(email_address)
    email = "Email: " + email_link
    email_line = surround_block('p', email)
    basic_information_line = name_line + email_line
    basic_information = surround_block('div', basic_information_line)
    content.append(basic_information)

    # projects
    projects_html = ''
    project_list = ''
    for project in projects:
        project_line = surround_block('li', project)
        project_list += project_line
    project_ul = surround_block('ul', project_list)
    project_header = surround_block('h2', 'Projects')
    project_content = project_header + project_ul
    project_div = surround_block('div', project_content)
    content.append(project_div)

    # Courses
    courses_header = surround_block('h3', "Courses")
    courses_line = ','.join(courses)
    courses_span = surround_block('span', courses_line)
    courses_content = courses_header + courses_span
    courses_div = surround_block('div', courses_content)
    content.append(courses_div)

    # close content
    content.append('</div></body></html>')

    return ''.join(content)



def generate_html(txt_input_file, html_output_file):
    """
    Loads given txt_input_file,
    gets the name, email address, list of projects, and list of courses,
    then writes the info to the given html_output_file.

    # Hint(s):
    # call function(s) to load given txt_input_file
    # call function(s) to get name
    # call function(s) to get email address
    # call function(s) to get list of projects
    # call function(s) to get list of courses
    # call function(s) to write the name, email address, list of projects, and list of courses to the given html_output_file
    """

    # insert code
    resume_template_content = read_resume_template('resume_template.html')
    student_info = read_student_info(txt_input_file)

    name = detect_name(student_info[0])
    email = detect_email(student_info[1:])
    courses = detect_courses(student_info[1:])
    projects = detect_projects(student_info[1:])
    content = get_resume_content(name, email, courses, projects)
    html_content = resume_template_content + content

    with open(html_output_file, 'w') as output_file:
        output_file.write(html_content)



def main():

    # DO NOT REMOVE OR UPDATE THIS CODE
    # generate resume.html file from provided sample resume.txt
    generate_html('resume.txt', 'resume.html')
    # print(read_student_info('resume.txt'))

    # generate_html('','')


    # DO NOT REMOVE OR UPDATE THIS CODE.
    # Uncomment each call to the generate_html function when you’re ready
    # to test how your program handles each additional test resume.txt file
    generate_html('TestResumes/resume_bad_name_lowercase/resume.txt', 'TestResumes/resume_bad_name_lowercase/resume.html')
    generate_html('TestResumes/resume_courses_w_whitespace/resume.txt', 'TestResumes/resume_courses_w_whitespace/resume.html')
    generate_html('TestResumes/resume_courses_weird_punc/resume.txt', 'TestResumes/resume_courses_weird_punc/resume.html')
    generate_html('TestResumes/resume_projects_w_whitespace/resume.txt', 'TestResumes/resume_projects_w_whitespace/resume.html')
    generate_html('TestResumes/resume_projects_with_blanks/resume.txt', 'TestResumes/resume_projects_with_blanks/resume.html')
    generate_html('TestResumes/resume_template_email_w_whitespace/resume.txt', 'TestResumes/resume_template_email_w_whitespace/resume.html')
    generate_html('TestResumes/resume_wrong_email/resume.txt', 'TestResumes/resume_wrong_email/resume.html')

    # If you want to test additional resume files, call the generate_html function with the given .txt file
    # and desired name of output .html file

if __name__ == '__main__':
    main()