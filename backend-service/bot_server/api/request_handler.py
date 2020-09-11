# TODO: Add Grade table and requests for it using patch
"""
This modules has functions to handle all the supported commands for the
classroom api's.

Author: Ayushi Rajendra Kumar
Date: 2020-09-02
"""
from .models import Course, Group, Student


def missing_field_error(field):
    error_response = {
        "status": 422,
        "message": f"Missing field {field}",
        "data": ""
    }
    return error_response


def create_new_course(data):
    return Course.objects.create_course(workspace_id=data["workspace_id"],
                                        course_name=data["course_name"],
                                        department=data["department"],
                                        semester=data["semester"],
                                        bot_token=data["bot_token"])


def get_course_details(workspace_id, data):
    data = Course.objects.get_course_details(workspace_id=workspace_id, course_name=data["course_name"],
                                             department=data["department"],
                                             semester=data["semester"])

    return {
        "status": 0,
        "message": "success",
        "data": data
    }


def get_all_courses(workspace_id):
    data = Course.objects.get_all_courses(workspace_id=workspace_id)

    return {
        "status": 0,
        "message": "success",
        "data": data
    }


def delete_course(data):
    return Course.objects.del_course(course_name=data["course_name"], department=data["department"])


def create_student(data):

    if 'unity_id' not in data:
        return missing_field_error('unity_id')
    if 'name' not in data:
        return missing_field_error('name')
    if 'email_id' not in data:
        return missing_field_error('email_id')

    if 'workspace_id' in data:
        course = Course.objects.get(workspace_id=data['workspace_id'])
    elif 'course_id' in data:
        course = Course.objects.get(log_course_id=data['course_id'])
    else:
        return missing_field_error("Course Identifier")

    return Student.objects.create_student(student_unity_id=data['unity_id'],
                                          course=course,
                                          name=data['name'],
                                          email_id=data['email_id'])


def update_student_details(data):

    if 'email_id' not in data:
        return missing_field_error('email_id')

    if 'workspace_id' in data:
        course = Course.objects.get(workspace_id=data['workspace_id'])
    elif 'course_id' in data:
        course = Course.objects.get(log_course_id=data['course_id'])
    else:
        return missing_field_error("Course Identifier")

    # TODO: Add bot token to response whenever 'workspace_id' in data else remove it

    response = None
    if 'group_num' in data:
        response = Student.objects.assign_group(email_id=data['email_id'], course=course, group_num=data['group_num'])
    elif 'slack_user_id' in data:
        response = Student.objects.update_slack_user_id(data['email_id'], course, data['slack_user_id'])
    else:
        response = missing_field_error('No field to update')
    return response


def get_student_details(email_id, workspace_id=None, course_id=None):

    if workspace_id is not None:
        course = Course.objects.get(workspace_id=workspace_id)
    elif course_id is not None:
        course = Course.objects.get(log_course_id=course_id)
    else:
        return missing_field_error("Course Identifier")

    response = Student.objects.get_student_details(email_id=email_id, course=course)

    # TODO: Add bot token whenever 'workspace_id' in data else remove it

    return {
        "status": 0,
        "message": "success",
        "data": response
    }


def delete_student(data):

    if 'email_id' not in data:
        return missing_field_error('email_id')

    if 'workspace_id' in data:
        course = Course.objects.get(workspace_id=data['workspace_id'])
    elif 'course_id' in data:
        course = Course.objects.get(log_course_id=data['course_id'])
    else:
        return missing_field_error("Course Identifier")

    return Student.objects.delete_student(email_id=data['email_id'], course=course)


def create_group(data):
    if 'group_num' not in data:
        return missing_field_error('group_num')

    response = Group.objects.create_group(group_num=data['group_num'], project_name=data['project_name'])
    return {
        "status": 0,
        "message": "success",
        "data": response
    }


def get_students_of_group(data):
    if 'group_num' not in data:
        return missing_field_error('group_num')

    response = Group.objects.get_students_of_group(data['group_num'])
    return {
        "status": 0,
        "message": "success",
        "data": response
    }