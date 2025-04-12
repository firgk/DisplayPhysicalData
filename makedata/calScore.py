

def calculate_score(student):
    # 计算BMI
    bmi = float(student.sWeight) / ((float(student.sHeight) / 100) ** 2)
    # 各项成绩占比
    bmi_weight = 0.15
    sVitalCapacity_weight = 0.15
    run50_weight = 0.2
    standingLongJump_weight = 0.1
    sittingForward_weight = 0.1
    run800_weight = 0.2
    run1000_weight = 0.2
    oneMinuteSitUps_weight = 0.1
    pullUP_weight = 0.1

    # 各项成绩原始分（这里简单假设为直接使用成绩数值，实际需根据评分标准转换）
    bmi_score = getBmi_score(student,bmi)
    sVitalCapacity_score = getsVitalCapacity_score(student)
    run50_score = getrun50_score(student)
    standingLongJump_score = getstandingLongJump_score(student)
    sittingForward_score = getsittingForward_score(student)
    run800_score = getrun800_score(student)
    run1000_score = getrun1000_score(student)
    oneMinuteSitUps_score = getoneMinuteSitUps_score(student)
    pullUP_score = getpullUP_score(student)



    # 计算总成绩
    # if student.sSex == '女':
    #     all_score = (
    #             bmi_score * bmi_weight +
    #             float(sVitalCapacity_score) * sVitalCapacity_weight +
    #             float(run50_score) * run50_weight +
    #             float(standingLongJump_score) * standingLongJump_weight +
    #             float(sittingForward_score) * sittingForward_weight +
    #             float(run800_score) * run800_weight +
    #             float(oneMinuteSitUps_score) * oneMinuteSitUps_weight
    #     )
    # 计算总成绩
    if student.sSex == '女':
        all_score = (
                (bmi_score if bmi_score is not None else 0) * bmi_weight +
                (float(sVitalCapacity_score) if sVitalCapacity_score is not None else 0) * sVitalCapacity_weight +
                (float(run50_score) if run50_score is not None else 0) * run50_weight +
                (float(standingLongJump_score) if standingLongJump_score is not None else 0) * standingLongJump_weight +
                (float(sittingForward_score) if sittingForward_score is not None else 0) * sittingForward_weight +
                (float(run800_score) if run800_score is not None else 0) * run800_weight +
                (float(oneMinuteSitUps_score) if oneMinuteSitUps_score is not None else 0) * oneMinuteSitUps_weight
        )
    elif student.sSex == '男':
        all_score = (
                bmi_score * bmi_weight +
                float(sVitalCapacity_score) * sVitalCapacity_weight +
                float(run50_score) * run50_weight +
                float(standingLongJump_score) * standingLongJump_weight +
                float(sittingForward_score) * sittingForward_weight +
                float(run1000_score) * run1000_weight +
                float(pullUP_score) * pullUP_weight
        )
    else:
        print("ERROR: 性别不明")

    student.score_bmi=bmi
    student.score_sVitalCapacity=student.sVitalCapacity
    student.score_run50=student.run50
    student.score_standingLongJump=student.standingLongJump
    student.score_sittingForward=student.sittingForward
    student.score_run800=student.run800
    student.score_run1000=student.run1000
    student.score_oneMinuteSitUps=student.oneMinuteSitUps
    student.score_pullUP=student.pullUP
    student.score_allScore=all_score

    return student






def getBmi_score(student,bmi):
    if student.sSex == '男':
    # 计算大学男生BMI成绩
        if 17.9 <= bmi <= 23.9:
            bmi_score = 100
        elif bmi <= 17.8:
            bmi_score = 80
        elif 24.0 <= bmi <= 27.9:
            bmi_score = 80
        else:
            bmi_score = 60
    elif student.sSex == '女':
    # 计算大学女生BMI成绩
        if 17.2 <= bmi <= 23.9:
            bmi_score = 100
        elif bmi <= 17.1:
            bmi_score = 80
        elif 24.0 <= bmi <= 27.9:
            bmi_score = 80
        else:
            bmi_score = 60
    else:
        bmi_score=0
    return bmi_score

def getsVitalCapacity_score(student):
    vital_capacity = int(student.sVitalCapacity)
    grade = student.grade
    if student.sSex== '男':
        if grade == '1':
            if vital_capacity >= 5040:
                return 100
            elif vital_capacity >= 4920:
                return 95
            elif vital_capacity >= 4800:
                return 90
            elif vital_capacity >= 4550:
                return 85
            elif vital_capacity >= 4400:
                return 80
            elif vital_capacity >= 4280:
                return 78
            elif vital_capacity >= 4160:
                return 76
            elif vital_capacity >= 4040:
                return 74
            elif vital_capacity >= 3920:
                return 72
            elif vital_capacity >= 3800:
                return 70
            elif vital_capacity >= 3680:
                return 68
            elif vital_capacity >= 3560:
                return 66
            elif vital_capacity >= 3440:
                return 64
            elif vital_capacity >= 3320:
                return 62
            elif vital_capacity >= 3200:
                return 60
            elif vital_capacity >= 3030:
                return 50
            elif vital_capacity >= 2860:
                return 40
            elif vital_capacity >= 2690:
                return 30
            elif vital_capacity >= 2520:
                return 20
            else:
                return 10
        elif grade == '2':
            if vital_capacity >= 5140:
                return 100
            elif vital_capacity >= 5020:
                return 95
            elif vital_capacity >= 4900:
                return 90
            elif vital_capacity >= 4650:
                return 85
            elif vital_capacity >= 4400:
                return 80
            elif vital_capacity >= 4280:
                return 78
            elif vital_capacity >= 4160:
                return 76
            elif vital_capacity >= 4040:
                return 74
            elif vital_capacity >= 3920:
                return 72
            elif vital_capacity >= 3800:
                return 70
            elif vital_capacity >= 3680:
                return 68
            elif vital_capacity >= 3560:
                return 66
            elif vital_capacity >= 3440:
                return 64
            elif vital_capacity >= 3320:
                return 62
            elif vital_capacity >= 3200:
                return 60
            elif vital_capacity >= 3030:
                return 50
            elif vital_capacity >= 2860:
                return 40
            elif vital_capacity >= 2690:
                return 30
            elif vital_capacity >= 2520:
                return 20
            else:
                return 10
        elif grade == '3':
            if vital_capacity >= 5140:
                return 100
            elif vital_capacity >= 5020:
                return 95
            elif vital_capacity >= 4900:
                return 90
            elif vital_capacity >= 4650:
                return 85
            elif vital_capacity >= 4400:
                return 80
            elif vital_capacity >= 4280:
                return 78
            elif vital_capacity >= 4160:
                return 76
            elif vital_capacity >= 4040:
                return 74
            elif vital_capacity >= 3920:
                return 72
            elif vital_capacity >= 3800:
                return 70
            elif vital_capacity >= 3680:
                return 68
            elif vital_capacity >= 3560:
                return 66
            elif vital_capacity >= 3440:
                return 64
            elif vital_capacity >= 3320:
                return 62
            elif vital_capacity >= 3200:
                return 60
            elif vital_capacity >= 3030:
                return 50
            elif vital_capacity >= 2860:
                return 40
            elif vital_capacity >= 2690:
                return 30
            elif vital_capacity >= 2520:
                return 20
            else:
                return 10
        elif grade == '4':
            if vital_capacity >= 5140:
                return 100
            elif vital_capacity >= 5020:
                return 95
            elif vital_capacity >= 4900:
                return 90
            elif vital_capacity >= 4650:
                return 85
            elif vital_capacity >= 4400:
                return 80
            elif vital_capacity >= 4280:
                return 78
            elif vital_capacity >= 4160:
                return 76
            elif vital_capacity >= 4040:
                return 74
            elif vital_capacity >= 3920:
                return 72
            elif vital_capacity >= 3800:
                return 70
            elif vital_capacity >= 3680:
                return 68
            elif vital_capacity >= 3560:
                return 66
            elif vital_capacity >= 3440:
                return 64
            elif vital_capacity >= 3320:
                return 62
            elif vital_capacity >= 3200:
                return 60
            elif vital_capacity >= 3030:
                return 50
            elif vital_capacity >= 2860:
                return 40
            elif vital_capacity >= 2690:
                return 30
            elif vital_capacity >= 2520:
                return 20
            else:
                return 10


        elif student.sSex=='女':
            if grade == '1':
                if vital_capacity >= 3400:
                    return 100
                elif vital_capacity >= 3350:
                    return 95
                elif vital_capacity >= 3300:
                    return 90
                elif vital_capacity >= 3150:
                    return 85
                elif vital_capacity >= 3000:
                    return 80
                elif vital_capacity >= 2900:
                    return 78
                elif vital_capacity >= 2800:
                    return 76
                elif vital_capacity >= 2700:
                    return 74
                elif vital_capacity >= 2600:
                    return 72
                elif vital_capacity >= 2500:
                    return 70
                elif vital_capacity >= 2400:
                    return 68
                elif vital_capacity >= 2300:
                    return 66
                elif vital_capacity >= 2200:
                    return 64
                elif vital_capacity >= 2100:
                    return 62
                elif vital_capacity >= 2000:
                    return 60
                elif vital_capacity >= 1960:
                    return 50
                elif vital_capacity >= 1920:
                    return 40
                elif vital_capacity >= 1880:
                    return 30
                elif vital_capacity >= 1840:
                    return 20
                else:
                    return 10
            elif grade == '2':
                if vital_capacity >= 3450:
                    return 100
                elif vital_capacity >= 3400:
                    return 95
                elif vital_capacity >= 3350:
                    return 90
                elif vital_capacity >= 3200:
                    return 85
                elif vital_capacity >= 3050:
                    return 80
                elif vital_capacity >= 2950:
                    return 78
                elif vital_capacity >= 2850:
                    return 76
                elif vital_capacity >= 2750:
                    return 74
                elif vital_capacity >= 2650:
                    return 72
                elif vital_capacity >= 2550:
                    return 70
                elif vital_capacity >= 2450:
                    return 68
                elif vital_capacity >= 2350:
                    return 66
                elif vital_capacity >= 2250:
                    return 64
                elif vital_capacity >= 2150:
                    return 62
                elif vital_capacity >= 2050:
                    return 60
                elif vital_capacity >= 2010:
                    return 50
                elif vital_capacity >= 1970:
                    return 40
                elif vital_capacity >= 1930:
                    return 30
                elif vital_capacity >= 1890:
                    return 20
                else:
                    return 10
            elif grade == '3':
                if vital_capacity >= 3450:
                    return 100
                elif vital_capacity >= 3400:
                    return 95
                elif vital_capacity >= 3350:
                    return 90
                elif vital_capacity >= 3200:
                    return 85
                elif vital_capacity >= 3050:
                    return 80
                elif vital_capacity >= 2950:
                    return 78
                elif vital_capacity >= 2850:
                    return 76
                elif vital_capacity >= 2750:
                    return 74
                elif vital_capacity >= 2650:
                    return 72
                elif vital_capacity >= 2550:
                    return 70
                elif vital_capacity >= 2450:
                    return 68
                elif vital_capacity >= 2350:
                    return 66
                elif vital_capacity >= 2250:
                    return 64
                elif vital_capacity >= 2150:
                    return 62
                elif vital_capacity >= 2050:
                    return 60
                elif vital_capacity >= 2010:
                    return 50
                elif vital_capacity >= 1970:
                    return 40
                elif vital_capacity >= 1930:
                    return 30
                elif vital_capacity >= 1890:
                    return 20
                else:
                    return 10
            elif grade == '4':
                if vital_capacity >= 3450:
                    return 100
                elif vital_capacity >= 3400:
                    return 95
                elif vital_capacity >= 3350:
                    return 90
                elif vital_capacity >= 3200:
                    return 85
                elif vital_capacity >= 3050:
                    return 80
                elif vital_capacity >= 2950:
                    return 78
                elif vital_capacity >= 2850:
                    return 76
                elif vital_capacity >= 2750:
                    return 74
                elif vital_capacity >= 2650:
                    return 72
                elif vital_capacity >= 2550:
                    return 70
                elif vital_capacity >= 2450:
                    return 68
                elif vital_capacity >= 2350:
                    return 66
                elif vital_capacity >= 2250:
                    return 64
                elif vital_capacity >= 2150:
                    return 62
                elif vital_capacity >= 2050:
                    return 60
                elif vital_capacity >= 2010:
                    return 50
                elif vital_capacity >= 1970:
                    return 40
                elif vital_capacity >= 1930:
                    return 30
                elif vital_capacity >= 1890:
                    return 20
                else:
                    return 10




def getrun50_score(student):
    run50 = float(student.run50)
    gender = student.sSex  # 假设student对象有gender属性来区分男女生
    grade = student.grade
    if gender == '男':
        if grade == '1':
            if run50 <= 6.7:
                return 100
            elif run50 <= 6.8:
                return 95
            elif run50 <= 6.9:
                return 90
            elif run50 <= 7.0:
                return 85
            elif run50 <= 7.1:
                return 80
            elif run50 <= 7.2:
                return 78
            elif run50 <= 7.3:
                return 76
            elif run50 <= 7.4:
                return 74
            elif run50 <= 7.5:
                return 72
            elif run50 <= 7.6:
                return 70
            elif run50 <= 7.7:
                return 68
            elif run50 <= 7.8:
                return 66
            elif run50 <= 7.9:
                return 64
            elif run50 <= 8.0:
                return 62
            elif run50 <= 8.1:
                return 60
            elif run50 <= 8.3:
                return 50
            elif run50 <= 8.5:
                return 40
            elif run50 <= 8.7:
                return 30
            elif run50 <= 8.9:
                return 20
            else:
                return 10
        elif grade == '2':
            if run50 <= 6.6:
                return 100
            elif run50 <= 6.7:
                return 95
            elif run50 <= 6.8:
                return 90
            elif run50 <= 6.9:
                return 85
            elif run50 <= 7.0:
                return 80
            elif run50 <= 7.1:
                return 78
            elif run50 <= 7.2:
                return 76
            elif run50 <= 7.3:
                return 74
            elif run50 <= 7.4:
                return 72
            elif run50 <= 7.5:
                return 70
            elif run50 <= 7.6:
                return 68
            elif run50 <= 7.7:
                return 66
            elif run50 <= 7.8:
                return 64
            elif run50 <= 7.9:
                return 62
            elif run50 <= 8.0:
                return 60
            elif run50 <= 8.3:
                return 50
            elif run50 <= 8.5:
                return 40
            elif run50 <= 8.7:
                return 30
            elif run50 <= 8.9:
                return 20
            else:
                return 10
        elif grade == '3':
            if run50 <= 6.6:
                return 100
            elif run50 <= 6.7:
                return 95
            elif run50 <= 6.8:
                return 90
            elif run50 <= 6.9:
                return 85
            elif run50 <= 7.0:
                return 80
            elif run50 <= 7.1:
                return 78
            elif run50 <= 7.2:
                return 76
            elif run50 <= 7.3:
                return 74
            elif run50 <= 7.4:
                return 72
            elif run50 <= 7.5:
                return 70
            elif run50 <= 7.6:
                return 68
            elif run50 <= 7.7:
                return 66
            elif run50 <= 7.8:
                return 64
            elif run50 <= 7.9:
                return 62
            elif run50 <= 8.0:
                return 60
            elif run50 <= 8.3:
                return 50
            elif run50 <= 8.5:
                return 40
            elif run50 <= 8.7:
                return 30
            elif run50 <= 8.9:
                return 20
            else:
                return 10
        elif grade == '4':
            if run50 <= 6.6:
                return 100
            elif run50 <= 6.7:
                return 95
            elif run50 <= 6.8:
                return 90
            elif run50 <= 6.9:
                return 85
            elif run50 <= 7.0:
                return 80
            elif run50 <= 7.1:
                return 78
            elif run50 <= 7.2:
                return 76
            elif run50 <= 7.3:
                return 74
            elif run50 <= 7.4:
                return 72
            elif run50 <= 7.5:
                return 70
            elif run50 <= 7.6:
                return 68
            elif run50 <= 7.7:
                return 66
            elif run50 <= 7.8:
                return 64
            elif run50 <= 7.9:
                return 62
            elif run50 <= 8.0:
                return 60
            elif run50 <= 8.3:
                return 50
            elif run50 <= 8.5:
                return 40
            elif run50 <= 8.7:
                return 30
            elif run50 <= 8.9:
                return 20
            else:
                return 10
    elif gender == '女':
        if grade == '1':
            if run50 <= 7.5:
                return 100
            elif run50 <= 7.6:
                return 95
            elif run50 <= 7.6:
                return 90
            elif run50 <= 8.0:
                return 85
            elif run50 <= 8.3:
                return 80
            elif run50 <= 8.4:
                return 78
            elif run50 <= 8.5:
                return 76
            elif run50 <= 8.6:
                return 74
            elif run50 <= 8.7:
                return 72
            elif run50 <= 8.8:
                return 70
            elif run50 <= 8.9:
                return 68
            elif run50 <= 9.0:
                return 66
            elif run50 <= 9.1:
                return 64
            elif run50 <= 9.2:
                return 62
            elif run50 <= 9.3:
                return 60
            elif run50 <= 9.5:
                return 50
            elif run50 <= 9.7:
                return 40
            elif run50 <= 9.9:
                return 30
            elif run50 <= 10.1:
                return 20
            else:
                return 10
        elif grade == '2':
            if run50 <= 7.4:
                return 100
            elif run50 <= 7.5:
                return 95
            elif run50 <= 7.6:
                return 90
            elif run50 <= 7.9:
                return 85
            elif run50 <= 8.2:
                return 80
            elif run50 <= 8.4:
                return 78
            elif run50 <= 8.5:
                return 76
            elif run50 <= 8.6:
                return 74
            elif run50 <= 8.7:
                return 72
            elif run50 <= 8.8:
                return 70
            elif run50 <= 8.9:
                return 68
            elif run50 <= 9.0:
                return 66
            elif run50 <= 9.1:
                return 64
            elif run50 <= 9.2:
                return 62
            elif run50 <= 9.3:
                return 60
            elif run50 <= 9.5:
                return 50
            elif run50 <= 9.7:
                return 40
            elif run50 <= 9.9:
                return 30
            elif run50 <= 10.1:
                return 20
            else:
                return 10
        elif grade == '3':
            if run50 <= 7.4:
                return 100
            elif run50 <= 7.5:
                return 95
            elif run50 <= 7.6:
                return 90
            elif run50 <= 7.9:
                return 85
            elif run50 <= 8.2:
                return 80
            elif run50 <= 8.4:
                return 78
            elif run50 <= 8.5:
                return 76
            elif run50 <= 8.6:
                return 74
            elif run50 <= 8.7:
                return 72
            elif run50 <= 8.8:
                return 70
            elif run50 <= 8.9:
                return 68
            elif run50 <= 9.0:
                return 66
            elif run50 <= 9.1:
                return 64
            elif run50 <= 9.2:
                return 62
            elif run50 <= 9.3:
                return 60
            elif run50 <= 9.5:
                return 50
            elif run50 <= 9.7:
                return 40
            elif run50 <= 9.9:
                return 30
            elif run50 <= 10.1:
                return 20
            else:
                return 10
        elif grade == '4':
            if run50 <= 7.4:
                return 100
            elif run50 <= 7.5:
                return 95
            elif run50 <= 7.6:
                return 90
            elif run50 <= 7.9:
                return 85
            elif run50 <= 8.2:
                return 80
            elif run50 <= 8.4:
                return 78
            elif run50 <= 8.5:
                return 76
            elif run50 <= 8.6:
                return 74
            elif run50 <= 8.7:
                return 72
            elif run50 <= 8.8:
                return 70
            elif run50 <= 8.9:
                return 68
            elif run50 <= 9.0:
                return 66
            elif run50 <= 9.1:
                return 64
            elif run50 <= 9.2:
                return 62
            elif run50 <= 9.3:
                return 60
            elif run50 <= 9.5:
                return 50
            elif run50 <= 9.7:
                return 40
            elif run50 <= 9.9:
                return 30
            elif run50 <= 10.1:
                return 20
            else:
                return 10

def getstandingLongJump_score(student):
    jump = float(student.standingLongJump)
    grade = student.grade
    gender = student.sSex
    if gender == "男":
        if grade == "1" or grade == "2":
            if jump >= 273:
                return 100
            elif jump >= 268:
                return 95
            elif jump >= 263:
                return 90
            elif jump >= 256:
                return 85
            elif jump >= 248:
                return 80
            elif jump >= 244:
                return 78
            elif jump >= 240:
                return 76
            elif jump >= 236:
                return 74
            elif jump >= 232:
                return 72
            elif jump >= 228:
                return 70
            elif jump >= 224:
                return 68
            elif jump >= 220:
                return 66
            elif jump >= 216:
                return 64
            elif jump >= 212:
                return 62
            elif jump >= 208:
                return 60
            elif jump >= 203:
                return 50
            elif jump >= 198:
                return 40
            elif jump >= 193:
                return 30
            elif jump >= 188:
                return 20
            elif jump >= 183:
                return 10
            else:
                return 0
        elif grade == "3" or grade == "4":
            if jump >= 275:
                return 100
            elif jump >= 270:
                return 95
            elif jump >= 265:
                return 90
            elif jump >= 258:
                return 85
            elif jump >= 250:
                return 80
            elif jump >= 246:
                return 78
            elif jump >= 242:
                return 76
            elif jump >= 238:
                return 74
            elif jump >= 234:
                return 72
            elif jump >= 230:
                return 70
            elif jump >= 226:
                return 68
            elif jump >= 222:
                return 66
            elif jump >= 218:
                return 64
            elif jump >= 214:
                return 62
            elif jump >= 210:
                return 60
            elif jump >= 205:
                return 50
            elif jump >= 200:
                return 40
            elif jump >= 195:
                return 30
            elif jump >= 190:
                return 20
            elif jump >= 185:
                return 10
            else:
                return 0
    elif gender == "女":
        if grade == "1" or grade == "2":
            if jump >= 207:
                return 100
            elif jump >= 201:
                return 95
            elif jump >= 195:
                return 90
            elif jump >= 188:
                return 85
            elif jump >= 181:
                return 80
            elif jump >= 178:
                return 78
            elif jump >= 175:
                return 76
            elif jump >= 172:
                return 74
            elif jump >= 169:
                return 72
            elif jump >= 166:
                return 70
            elif jump >= 163:
                return 68
            elif jump >= 160:
                return 66
            elif jump >= 157:
                return 64
            elif jump >= 154:
                return 62
            elif jump >= 151:
                return 60
            elif jump >= 146:
                return 50
            elif jump >= 141:
                return 40
            elif jump >= 136:
                return 30
            elif jump >= 131:
                return 20
            elif jump >= 126:
                return 10
            else:
                return 0
        elif grade == "3" or grade == "4":
            if jump >= 208:
                return 100
            elif jump >= 202:
                return 95
            elif jump >= 196:
                return 90
            elif jump >= 189:
                return 85
            elif jump >= 182:
                return 80
            elif jump >= 179:
                return 78
            elif jump >= 176:
                return 76
            elif jump >= 173:
                return 74
            elif jump >= 170:
                return 72
            elif jump >= 167:
                return 70
            elif jump >= 164:
                return 68
            elif jump >= 161:
                return 66
            elif jump >= 158:
                return 64
            elif jump >= 155:
                return 62
            elif jump >= 152:
                return 60
            elif jump >= 147:
                return 50
            elif jump >= 142:
                return 40
            elif jump >= 137:
                return 30
            elif jump >= 132:
                return 20
            elif jump >= 127:
                return 10
            else:
                return 0


# 假设student是一个类的实例，具有sittingForward（坐位体前屈成绩）、grade（年级）、gender（性别）属性
def getsittingForward_score(student):
    sittingForward = float(student.sittingForward)
    grade = student.grade
    gender = student.sSex
    if gender == '男':
        if grade in ['1', '2']:
            if sittingForward >= 24.9:
                return 100
            elif sittingForward >= 23.1:
                return 95
            elif sittingForward >= 21.3:
                return 90
            elif sittingForward >= 19.5:
                return 85
            elif sittingForward >= 18.2:
                return 80
            elif sittingForward >= 16.8:
                return 78
            elif sittingForward >= 15.4:
                return 76
            elif sittingForward >= 14.0:
                return 74
            elif sittingForward >= 12.6:
                return 72
            elif sittingForward >= 11.2:
                return 70
            elif sittingForward >= 9.8:
                return 68
            elif sittingForward >= 8.4:
                return 66
            elif sittingForward >= 7.0:
                return 64
            elif sittingForward >= 5.6:
                return 62
            elif sittingForward >= 4.2:
                return 60
            elif sittingForward >= 3.2:
                return 50
            elif sittingForward >= 2.2:
                return 40
            elif sittingForward >= 1.2:
                return 30
            elif sittingForward >= 0.2:
                return 20
            else:
                return 10
        elif grade in ['3', '4']:
            if sittingForward >= 25.3:
                return 100
            elif sittingForward >= 23.3:
                return 95
            elif sittingForward >= 21.5:
                return 90
            elif sittingForward >= 19.9:
                return 85
            elif sittingForward >= 18.2:
                return 80
            elif sittingForward >= 16.8:
                return 78
            elif sittingForward >= 15.4:
                return 76
            elif sittingForward >= 14.0:
                return 74
            elif sittingForward >= 12.6:
                return 72
            elif sittingForward >= 11.2:
                return 70
            elif sittingForward >= 9.8:
                return 68
            elif sittingForward >= 8.4:
                return 66
            elif sittingForward >= 7.0:
                return 64
            elif sittingForward >= 5.6:
                return 62
            elif sittingForward >= 4.2:
                return 60
            elif sittingForward >= 3.2:
                return 50
            elif sittingForward >= 2.2:
                return 40
            elif sittingForward >= 1.2:
                return 30
            elif sittingForward >= 0.2:
                return 20
            else:
                return 10
    elif gender == '女':
        if grade in ['1', '2']:
            if sittingForward >= 25.8:
                return 100
            elif sittingForward >= 24.0:
                return 95
            elif sittingForward >= 22.2:
                return 90
            elif sittingForward >= 20.6:
                return 85
            elif sittingForward >= 19.0:
                return 80
            elif sittingForward >= 18.2:
                return 78
            elif sittingForward >= 16.9:
                return 76
            elif sittingForward >= 15.6:
                return 74
            elif sittingForward >= 14.3:
                return 72
            elif sittingForward >= 13.0:
                return 70
            elif sittingForward >= 11.2:
                return 68
            elif sittingForward >= 9.9:
                return 66
            elif sittingForward >= 8.6:
                return 64
            elif sittingForward >= 7.3:
                return 62
            elif sittingForward >= 6.0:
                return 60
            elif sittingForward >= 5.2:
                return 50
            elif sittingForward >= 4.2:
                return 40
            elif sittingForward >= 3.6:
                return 30
            elif sittingForward >= 2.8:
                return 20
            else:
                return 10
        elif grade in ['3', '4']:
            if sittingForward >= 26.3:
                return 100
            elif sittingForward >= 24.4:
                return 95
            elif sittingForward >= 22.4:
                return 90
            elif sittingForward >= 21.0:
                return 85
            elif sittingForward >= 19.5:
                return 80
            elif sittingForward >= 18.2:
                return 78
            elif sittingForward >= 16.9:
                return 76
            elif sittingForward >= 15.6:
                return 74
            elif sittingForward >= 14.3:
                return 72
            elif sittingForward >= 13.0:
                return 70
            elif sittingForward >= 11.7:
                return 68
            elif sittingForward >= 10.4:
                return 66
            elif sittingForward >= 9.1:
                return 64
            elif sittingForward >= 7.8:
                return 62
            elif sittingForward >= 6.5:
                return 60
            elif sittingForward >= 5.7:
                return 50
            elif sittingForward >= 4.9:
                return 40
            elif sittingForward >= 4.1:
                return 30
            elif sittingForward >= 3.3:
                return 20
            else:
                return 10

def getrun800_score(student):
    grade = student.grade
    if student.sSex == '女' and (grade in ['1', '2']):
        run800 = float(student.run800)
        # 将时间区间转换为秒
        time_score_intervals = [
            ((196, 198), 100),
            ((202, 204), 95),
            ((208, 210), 90),
            ((215, 217), 85),
            ((222, 224), 80),
            ((227, 229), 78),
            ((232, 234), 76),
            ((237, 239), 74),
            ((242, 244), 72),
            ((247, 249), 70),
            ((252, 254), 68),
            ((257, 259), 66),
            ((262, 264), 64),
            ((267, 269), 62),
            ((272, 274), 60),
            ((282, 284), 50),
            ((292, 294), 40),
            ((302, 304), 30),
            ((312, 314), 20),
            ((322, 324), 10)
        ]
        for interval, score in time_score_intervals:
            start_time, end_time = interval
            if start_time <= run800 <= end_time:
                return score
        return 0
    return 0



def getrun1000_score(student):
    grade = student.grade
    if student.sSex == '男' and (grade in ['1', '2']):
        run1000 = float(student.run1000)
        time_score_intervals = [
            ((195, 197), 100),
            ((200, 202), 95),
            ((205, 207), 90),
            ((212, 214), 85),
            ((220, 222), 80),
            ((225, 227), 78),
            ((230, 232), 76),
            ((235, 237), 74),
            ((240, 242), 72),
            ((245, 247), 70),
            ((250, 252), 68),
            ((255, 257), 66),
            ((260, 262), 64),
            ((265, 267), 62),
            ((270, 272), 60),
            ((290, 292), 50),
            ((310, 312), 40),
            ((330, 332), 30),
            ((350, 352), 20),
            ((370, 372), 10)
        ]
        for interval, score in time_score_intervals:
            start_time, end_time = interval
            if start_time <= run1000 <= end_time:
                return score
        return 0
    return 0


def getoneMinuteSitUps_score(student):
    grade = student.grade
    if student.sSex == '女':
        oneMinuteSitUps = int(student.oneMinuteSitUps)
        if grade in ['1', '2']:
            if oneMinuteSitUps >= 56:
                score = 100
            elif oneMinuteSitUps >= 54:
                score = 95
            elif oneMinuteSitUps >= 52:
                score = 90
            elif oneMinuteSitUps >= 50:
                score = 85
            elif oneMinuteSitUps >= 48:
                score = 80
            elif oneMinuteSitUps >= 46:
                score = 78
            elif oneMinuteSitUps >= 44:
                score = 76
            elif oneMinuteSitUps >= 42:
                score = 74
            elif oneMinuteSitUps >= 40:
                score = 72
            elif oneMinuteSitUps >= 38:
                score = 70
            elif oneMinuteSitUps >= 36:
                score = 68
            elif oneMinuteSitUps >= 34:
                score = 66
            elif oneMinuteSitUps >= 32:
                score = 64
            elif oneMinuteSitUps >= 30:
                score = 62
            elif oneMinuteSitUps >= 28:
                score = 60
            elif oneMinuteSitUps >= 26:
                score = 50
            elif oneMinuteSitUps >= 24:
                score = 40
            elif oneMinuteSitUps >= 22:
                score = 30
            elif oneMinuteSitUps >= 20:
                score = 20
            elif oneMinuteSitUps >= 18:
                score = 10
            else:
                score = 0
        elif grade in ['3', '4']:
            if oneMinuteSitUps >= 57:
                score = 100
            elif oneMinuteSitUps >= 55:
                score = 95
            elif oneMinuteSitUps >= 53:
                score = 90
            elif oneMinuteSitUps >= 50:
                score = 85
            elif oneMinuteSitUps >= 48:
                score = 80
            elif oneMinuteSitUps >= 46:
                score = 78
            elif oneMinuteSitUps >= 44:
                score = 76
            elif oneMinuteSitUps >= 42:
                score = 74
            elif oneMinuteSitUps >= 40:
                score = 72
            elif oneMinuteSitUps >= 38:
                score = 70
            elif oneMinuteSitUps >= 36:
                score = 68
            elif oneMinuteSitUps >= 34:
                score = 66
            elif oneMinuteSitUps >= 32:
                score = 64
            elif oneMinuteSitUps >= 30:
                score = 62
            elif oneMinuteSitUps >= 28:
                score = 60
            elif oneMinuteSitUps >= 26:
                score = 50
            elif oneMinuteSitUps >= 24:
                score = 40
            elif oneMinuteSitUps >= 22:
                score = 30
            elif oneMinuteSitUps >= 20:
                score = 20
            elif oneMinuteSitUps >= 18:
                score = 10
            else:
                score = 0
        else:
            score = 0
        return score

def getpullUP_score(student):
    grade = student.grade
    if student.sSex == '男':
        pullUP = int(student.pullUP)
        if grade in ['1', '2']:
            if pullUP >= 19:
                score = 100
            elif pullUP >= 18:
                score = 95
            elif pullUP >= 17:
                score = 90
            elif pullUP >= 16:
                score = 85
            elif pullUP >= 15:
                score = 80
            elif pullUP >= 14:
                score = 78
            elif pullUP >= 13:
                score = 76
            elif pullUP >= 12:
                score = 74
            elif pullUP >= 11:
                score = 72
            elif pullUP >= 10:
                score = 70
            elif pullUP >= 9:
                score = 68
            elif pullUP >= 8:
                score = 66
            elif pullUP >= 7:
                score = 64
            elif pullUP >= 6:
                score = 62
            elif pullUP >= 5:
                score = 60
            elif pullUP >= 4:
                score = 50
            elif pullUP >= 3:
                score = 40
            elif pullUP >= 2:
                score = 30
            elif pullUP >= 1:
                score = 20
            else:
                score = 10
        elif grade in ['3', '4']:
            if pullUP >= 20:
                score = 100
            elif pullUP >= 19:
                score = 95
            elif pullUP >= 18:
                score = 90
            elif pullUP >= 17:
                score = 85
            elif pullUP >= 16:
                score = 80
            elif pullUP >= 15:
                score = 78
            elif pullUP >= 14:
                score = 76
            elif pullUP >= 13:
                score = 74
            elif pullUP >= 12:
                score = 72
            elif pullUP >= 11:
                score = 70
            elif pullUP >= 10:
                score = 68
            elif pullUP >= 9:
                score = 66
            elif pullUP >= 8:
                score = 64
            elif pullUP >= 7:
                score = 62
            elif pullUP >= 6:
                score = 60
            elif pullUP >= 5:
                score = 50
            elif pullUP >= 4:
                score = 40
            elif pullUP >= 3:
                score = 30
            elif pullUP >= 2:
                score = 20
            elif pullUP >= 1:
                score = 10
            else:
                score = 0
        else:
            score = 0
        return score

