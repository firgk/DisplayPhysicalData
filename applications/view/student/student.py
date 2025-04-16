from flask import Blueprint, render_template, request, redirect,jsonify
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role, College
from applications.models import User, AdminLog, Student

bp = Blueprint('student', __name__, url_prefix='/student')




# 体测成绩
@bp.get('/data/')
@authorize("student:data")
def data():
    colleges = College.query.all()
    return render_template('student/data/main.html',colleges=colleges)



@bp.get('/data/college')
@authorize("student:data")
def dataCollege():
    colleges = College.query.all()
    return jsonify([{
        'id': college.id,
        'collegeCode': college.collegeCode,
        'className': college.className
    } for college in colleges])




# 学生信息
@bp.get('/data/data')
@authorize("student:data")
def dataData():
    # 获取请求参数 姓名 学号
    real_name = str_escape(request.args.get('realname', type=str))
    username = str_escape(request.args.get('username', type=str))

    filters = []
    if real_name:
        filters.append(Student.sName.contains(real_name))
    if username:
        filters.append(Student.sNumber.contains(username))

    # print(*filters)
    query = db.session.query(
        Student
    ).filter(*filters).layui_paginate()

    return table_api(
        data=[{
            'id': student.id,
            'sName': student.sName,
            'sNumber': student.sNumber,
            'sSex': student.sSex,
            'sHeight': student.sHeight,
            'sWeight': student.sWeight,
            'sVitalCapacity': student.sVitalCapacity,
            'run50': student.run50,
            'standingLongJump': student.standingLongJump,
            'sittingForward': student.sittingForward,
            'run800': student.run800,
            'run1000': student.run1000,
            'oneMinuteSitUps': student.oneMinuteSitUps,
            'pullUP': student.pullUP,
            'update_at': student.update_at,
            'score_bmi': student.score_bmi,
            'score_sVitalCapacity': student.score_sVitalCapacity,
            'score_run50': student.score_run50,
            'score_standingLongJump': student.score_standingLongJump,
            'score_sittingForward': student.score_sittingForward,
            'score_run800': student.score_run800,
            'score_run1000': student.score_run1000,
            'score_oneMinuteSitUps': student.score_oneMinuteSitUps,
            'score_pullUP': student.score_pullUP,
            'score_allScore': student.score_allScore,
            'score_error': student.score_error,
            'score_errormessage': student.score_errormessage,
        } for student in query.items],
        count=query.total)






@bp.get('/data/add/')
@authorize("student:add")
def dataAdd():
    return render_template('student/data/edit.html')



#  编辑用户
@bp.post('/data/save/')
# @authorize("student:add")
def dataSave():

    req_json = request.get_json(force=True)

    sNumber = str_escape(req_json.get('sNumber'))
    sName = str_escape(req_json.get('sName'))
    sHeight = str_escape(req_json.get('sHeight'))
    sWeight = str_escape(req_json.get('sWeight'))
    sVitalCapacity = str_escape(req_json.get('sVitalCapacity'))
    run50 = str_escape(req_json.get('run50'))
    standingLongJump = str_escape(req_json.get('standingLongJump'))
    sittingForward = str_escape(req_json.get('sittingForward'))
    run800 = str_escape(req_json.get('run800'))
    run1000 = str_escape(req_json.get('run1000'))
    oneMinuteSitUps = str_escape(req_json.get('oneMinuteSitUps'))
    pullUP = str_escape(req_json.get('pullUP'))


    if not sNumber or not sName:
        print(sNumber, sName)
        return fail_api(msg="学生姓名或学号不能为空")


    filters = []
    filters.append(Student.sName.contains(sName))
    filters.append(Student.sNumber.contains(sNumber))

    student = Student.query.filter(*filters).first()

    if not student:
        return fail_api(msg="学生不存在")

    update_data = {}
    if sHeight:
        update_data['sHeight'] = sHeight
    if sWeight:
        update_data['sWeight'] = sWeight
    if sVitalCapacity:
        update_data['sVitalCapacity'] = sVitalCapacity
    if run50:
        update_data['run50'] = run50
    if standingLongJump:
        update_data['standingLongJump'] = standingLongJump
    if sittingForward:
        update_data['sittingForward'] = sittingForward
    if run800:
        update_data['run800'] = run800
    if run1000:
        update_data['run1000'] = run1000
    if oneMinuteSitUps:
        update_data['oneMinuteSitUps'] = oneMinuteSitUps
    if pullUP:
        update_data['pullUP'] = pullUP

    Student.query.filter_by(sName=sName, sNumber=sNumber).update(update_data)

    # result = Student.query.filter_by(sName=sName, sNumber=sNumber).update(update_data)
    # if result == 0:
    #     print(f"调试信息: 更新失败，未找到匹配的学生记录，sName: {sName}, sNumber: {sNumber}")
    # else:
    #     print(f"调试信息: 更新成功，更新了 {result} 条记录")


    db.session.commit()
    return success_api(msg="添加成功")




#  编辑用户
@bp.get('/data/edit/<int:id>')
@authorize("student:data")
def dataEdit(id):
    student = curd.get_one_by_id(Student, id)
    colleges = College.query.all()
    return render_template('student/edit.html', student=student, colleges=colleges)







# 数据分析
@bp.get('/show_small/')
@authorize("student:show_small")
def show_small():
    return render_template('student/show/index_small.html')



@bp.get('/add/')
@authorize("student:add")
def add():
    return redirect('/student/info/add/')






# 学生信息
@bp.get('/info/')
@authorize("student:info")
def info():
    colleges = College.query.all()
    return render_template('student/main.html',colleges=colleges)




# 学生信息
@bp.get('/info/college')
@authorize("student:info")
def infoCollege():
    colleges = College.query.all()
    return jsonify([{
        'id': college.id,
        'collegeCode': college.collegeCode,
        'className': college.className
    } for college in colleges])




# 学生信息
@bp.get('/info/data')
@authorize("student:info")
def infoData():
    # 获取请求参数 姓名 学号
    real_name = str_escape(request.args.get('realname', type=str))
    username = str_escape(request.args.get('username', type=str))
    classNum = str_escape(request.args.get('classNum', type=str))
    grade = str_escape(request.args.get('grade', type=str))
    collegeCode = str_escape(request.args.get('collegeCode', type=str))


    filters = []
    if real_name:
        filters.append(Student.sName.contains(real_name))
    if username:
        filters.append(Student.sNumber.contains(username))
    if classNum:
        filters.append(Student.classNum.contains(classNum))
    if grade:
        filters.append(Student.grade.contains(grade))
    if collegeCode:
        filters.append(Student.collegeCode.contains(collegeCode))



    # print(*filters)
    query = db.session.query(
        Student
    ).filter(*filters).layui_paginate()

    return table_api(
        data=[{
            'id': student.id,
            'sName': student.sName,
            'sNumber': student.sNumber,
            'sSex': student.sSex,
            'collegeCode': student.collegeCode,
            'grade': student.grade,
            'classNum': student.classNum,
            'enable': student.enable,
            'sBirthDate': student.sBirthDate,
        } for student in query.items],
        count=query.total)


#  编辑用户
@bp.get('/info/edit/<int:id>')
@authorize("student:info")
def infoEdit(id):
    student = curd.get_one_by_id(Student, id)
    colleges = College.query.all()
    return render_template('student/edit.html', student=student, colleges=colleges)


#  编辑用户
@bp.put('/info/update/')
@authorize("student:info")
def infoUpdate():
    req_json = request.get_json(force=True)
    id = str_escape(req_json.get("userId"))
    sNumber = str_escape(req_json.get('sNumber'))
    sName = str_escape(req_json.get('sName'))
    sSex = str_escape(req_json.get('sSex'))
    collegeCode = str_escape(req_json.get('collegeCode'))
    grade = str_escape(req_json.get('grade'))
    classNum = str_escape(req_json.get('classNum'))
    sBirthDate = str_escape(req_json.get('sBirthDate'))
    Student.query.filter_by(id=id).update(
        {'sNumber': sNumber, 'sName': sName, 'sSex': sSex, 'collegeCode': collegeCode, 'grade': grade,
         'classNum': classNum, 'sBirthDate': sBirthDate})
    db.session.commit()
    return success_api(msg="更新成功")


# 启用用户
@bp.put('/info/enable')
def enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = enable_status(model=Student, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用用户
@bp.put('/info/disable')
def dis_enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = disable_status(model=Student, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 成绩录入
@bp.get('/info/add/')
@authorize("student:add")
def infoAdd():
    colleges = College.query.all()
    return render_template('student/add.html', colleges=colleges)


@bp.post('/info/save/')
@authorize("student:info")
def infoSave():
    req_json = request.get_json(force=True)

    sNumber = str_escape(req_json.get('sNumber'))
    sName = str_escape(req_json.get('sName'))
    password = str_escape(req_json.get('password'))
    sSex = str_escape(req_json.get('sSex'))
    collegeCode = str_escape(req_json.get('collegeCode'))
    grade = str_escape(req_json.get('grade'))
    classNum = str_escape(req_json.get('classNum'))
    sBirthDate = str_escape(req_json.get('sBirthDate'))

    if not sNumber or not sName or not password:
        return fail_api(msg="账号姓名密码不得为空")

    if bool(Student.query.filter_by(sNumber=sNumber).count()):
        return fail_api(msg="该学号学生已经存在")

    student = Student(sNumber=sNumber, sName=sName, enable=1, sSex=sSex, collegeCode=collegeCode, grade=grade,
                      classNum=classNum, sBirthDate=sBirthDate)
    student.set_password(password)
    db.session.add(student)

    db.session.commit()
    return success_api(msg="增加成功")




# 大屏展示
@bp.get('/show/')
@authorize("student:show")
def show():
    return render_template('student/show/index.html')





































