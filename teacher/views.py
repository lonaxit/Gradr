from django.shortcuts import render,redirect


from django.http import HttpResponse,JsonResponse


# import models
# from accounts.models import *
# from administrator.models import *
from accounts.models import Client,Student
from administrator.models import Session,Term,StudentClass,Subject,SubjectTeacher,ClassTeacher
from .models import *
from django.db.models import Q, Sum, Avg, Max, Min
# import for user registration form
from  django.contrib.auth.forms import UserCreationForm
# from accounts.forms import ClientRegisterForm, contactForm, ClientForm,StudentRegisterForm
from accounts.forms import *
# from administrator.forms import TermForm,SessionForm
from administrator.forms import *
from teacher.forms import *
from django.contrib import messages
#import for restricting access to pages
from django.contrib.auth.decorators import login_required

# import for creating a group
from django.contrib.auth.models import Group


#custom decorator
from accounts.decorators import unauthenticated_user,allowed_users,admin_only
# Create your views here.

@login_required(login_url='login')
# @admin_only
@allowed_users(allowed_roles=['teacher'])
def teacherHome(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request,'teacher/teacher_home.html',context)


# add new scores
@allowed_users(allowed_roles=['teacher'])
def addScores(request):

    loggedin = request.user.teacher

    form = ScoresForm()

    context = {'form':form}
    if request.method =='POST':
        subj = request.POST['subject']
        studclass = request.POST['studentclass']
        studid = request.POST['studentnumber']
        ca1 = request.POST['firstscore']
        ca2 = request.POST['secondscore']
        ca3 = request.POST['thirdscore']
        totalass = request.POST['totalca']
        exam = request.POST['examscore']
        total = request.POST['subjecttotal']

        # get sctive term and session
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')

        teacherObj = SubjectTeacher.objects.get(pk=loggedin.id)
        subjectObj = Subject.objects.get(pk=subj)
        classroomObj = StudentClass.objects.get(pk=studclass)
        studObj = Student.objects.get(pk=studid)


        # check if record for the subject exist
        scores = Scores.objects.filter(Q(term=activeTerm) & Q(studentclass=classroomObj)
        & Q(session=activeSession) & Q(subject=subjectObj) & Q(student=studObj) )

        if scores:
            messages.error(request, 'Record exist')
            return redirect('new-scores')
        else:
            obj = Scores.objects.create(
                                 firstscore = ca1,
                                 secondscore = ca2,
                                 thirdscore = ca3,
                                 totalca = totalass,
                                 examscore = exam,
                                 session = activeSession,
                                 studentclass = classroomObj,
                                 subject = subjectObj,
                                 subjectteacher = teacherObj,
                                 term = activeTerm,
                                 subjecttotal = total,
                                 client = loggedin.client,
                                 student = studObj,
                                     )
            obj.save()
            
            # process Scores
            processScores(subjectObj,classroomObj)
            
            # process terminal result
            processTerminalResult(obj)
             
            messages.success(request, 'Scores created')
            # return redirect('assign-subject')
    # context = {'form':form}
    return render(request,'teacher/new_scores.html',context)


# edit scores
@allowed_users(allowed_roles=['teacher'])
def editScores(request,id):

    loggedin = request.user.teacher
    scores = Scores.objects.get(pk=id)
    form = ScoresForm(instance=scores)
    # student = Student.objects.get(id=scores.student.id)

    context = {'form':form,'scores':scores}
    if request.method =='POST':


        # form = ScoresForm(request.POST,instance=scores)
        subj = request.POST['subject']
        studclass = request.POST['studentclass']
        studid = request.POST['studentnumber']

        ca1 = request.POST['firstscore']
        ca2 = request.POST['secondscore']
        ca3 = request.POST['thirdscore']
        totalass = request.POST['totalca']
        exam = request.POST['examscore']
        total = request.POST['subjecttotal']

        # get active term and session
        activeTerm = Term.objects.get(status='True')
        activeSession = Session.objects.get(status='True')

        teacherObj = SubjectTeacher.objects.get(pk=loggedin.id)
        subjectObj = Subject.objects.get(pk=subj)
        classroomObj = StudentClass.objects.get(pk=studclass)
        studObj = Student.objects.get(pk=studid)
        
        
        scores.firstscore = ca1
        scores.secondscore = ca2
        scores.thirdscore = ca3
        scores.totalca = totalass
        scores.examscore = exam
        scores.session = activeSession
        scores.studentclass = classroomObj
        scores.subject = subjectObj
        scores.subjectteacher = teacherObj
        scores.term = activeTerm
        scores.subjecttotal = total
        scores.client = loggedin.client
        scores.student = studObj
        scores.save()
        
        # print(scores.firstscore)
        
        # process Scores
        processScores(subjectObj,classroomObj)
        
        # process terminal result
        processTerminalResult(scores)
        
        # Scores.objects.filter(id=data['id']).update(email=data['email'], phone=data['phone'])
        messages.success(request, 'Scores edited successfully')
        return redirect('filter-scores')
    # context = {'form':form}
    return render(request,'teacher/edit_scores.html',context)

# remove scores

@allowed_users(allowed_roles=['teacher'])
def deleteScores(request,id):

    loggedin = request.user.teacher
    scores = Scores.objects.get(pk=id)
    
    # get sctive term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')
    
    subject = scores.subject
    classroom = scores.studentclass
    studentid = scores.student
    
    scores.delete()
    
    # delete terminal result
    deleteResult(studentid,classroom)
    scores_filter = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession).first()
    
    if scores_filter:
        # process Scores
        processScores(subject,classroom)
        # process terminal result
        processTerminalResult(scores_filter)
        
        # TODO: MAKE SURE TO DELETE CORRESPONDING STUDENT RECORD IN THE RESULT TABLE
        
    messages.success(request, 'Scores deleted successfully')
    return redirect('filter-scores')
    
    # return render(request,'teacher/edit_scores.html')


# Filter Scores
@allowed_users(allowed_roles=['teacher'])
def scoresFilter(request):

    loggedin = request.user.teacher

    form = ScoresFilterForm()


    if request.method =='POST':

        classroom = request.POST['classroom']
        subject = request.POST['subject']
        session = request.POST['session']
        term = request.POST['term']


        # get sctive term and session
        # activeTerm = Term.objects.get(status='True')
        # activeSession = Session.objects.get(status='True')
        #
        # teacherObj = SubjectTeacher.objects.get(id=loggedin.id)
        # subjectObj = Subject.objects.get(id=subj)
        # classroomObj = StudentClass.objects.get(id=studclass)
        # studObj = Student.objects.get(id=studid)

        # check if record for the subject exist
        scores = Scores.objects.filter(Q(term=term) & Q(studentclass=classroom)
        & Q(session=session) & Q(subject=subject))

        #
        if not scores:
            messages.error(request, 'No record exist')
            return redirect('filter-scores')
        else:
            context ={ 'form':form,'scores':scores}
            return render(request,'teacher/filterScores.html',context)
    context = {'form':form}
    return render(request,'teacher/filterScores.html',context)


# Result Filter
@allowed_users(allowed_roles=['teacher'])
def resultFilter(request):

    loggedin = request.user.teacher.pk

    form = ResultFilterForm()
    # entry = ClassTeacher.objects.filter(teacher=loggedin)
    
        

    if request.method =='POST':
        
        if request.POST.get('result-id'):
            
            # print
            resultObj = Result.objects.get(pk=request.POST['result-id'])
            # select all result that fit criteria
            result = Result.objects.filter(Q(term=resultObj.term) & Q(studentclass=resultObj.studentclass)
            & Q(session=resultObj.session)).order_by('termposition')
            
            # save/update comment here
            comment = request.POST['comment']
            
            resultObj.classteachercomment=comment
            resultObj.save()
            
            messages.success(request, 'Comment added')
            
            context ={ 'form':form,'result':result}
            return render(request,'teacher/filterResult.html',context)

            
            
        else:
            classroom = request.POST['classroom']
            session = request.POST['session']
            term = request.POST['term']

            if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():
                
                # select reesult
                result = Result.objects.filter(Q(term=term) & Q(studentclass=classroom)
                & Q(session=session)).order_by('termposition')

                #check for availability of result
                if not result:
                    messages.error(request, 'No record exist')
                    return redirect('filter-result')
                else:
                    
                    context ={ 'form':form,'result':result}
                    return render(request,'teacher/filterResult.html',context)
    context = {'form':form}
    return render(request,'teacher/filterResult.html',context)

# Add comment
@allowed_users(allowed_roles=['teacher'])
def addComment(request):

    loggedin = request.user.teacher.pk

    form = ResultFilterForm()
    # entry = ClassTeacher.objects.filter(teacher=loggedin)
    
        

    if request.method =='POST':

        classroom = request.POST['classroom']
        session = request.POST['session']
        term = request.POST['term']

        if ClassTeacher.objects.filter(teacher=loggedin,classroom=classroom,session=session,term=term).exists():
            
            # select reesult
            result = Result.objects.filter(Q(term=term) & Q(term=term) & Q(studentclass=classroom)
            & Q(session=session)).order_by('termposition')

            #check for availability of result
            if not result:
                
                messages.error(request, 'No record exist')
                return redirect('filter-result')
            else:
                
                context ={ 'form':form,'result':result}
                return render(request,'teacher/filterResult.html',context)
    context = {'form':form}
    return render(request,'teacher/filterResult.html',context)

# get subjects on class change
def get_subjects(request,pk):
    loggedin = request.user.teacher

    result = list(Subject.objects.filter(subjectteacher__classroom_id=pk).filter(subjectteacher__teacher_id=loggedin.id).values())
    #lg_data = list(Lga.objects.filter(state_id=pk).values())


    return JsonResponse({'data':result})

# find subject and class average
def subjectAverage(subj,classroom):
    # scores = Scores.objects.get(pk=id)
    # get sctive term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    # get scores based on subject
    # scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).distinct('student').aggregate(Sum('subjAverage'))
    
    scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).aggregate(scoresav=Avg('subjecttotal'))
    
    av = scores['scoresav']
    
    # scoresAv = scores.aggregate(Sum('subjAverage'))
    
    return av


# terminal average 
def terminalAverage(studentid,classroom):
    
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    # get scores based on subject
    # scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).distinct('student').aggregate(Sum('subjAverage'))
    
    scores = Scores.objects.filter(student=studentid,studentclass=classroom,term=activeTerm,session=activeSession).aggregate(term_sum=Sum('subjecttotal'))
    
    term_sum = scores['term_sum']
    # get subject per class
    no_subj_per_class = SubjectPerClass.objects.get(sch_class=classroom)
    
    class_av = term_sum/no_subj_per_class.no_subject
    
    # TODO MOVE CODE TO UPDATE TERMINAL AVERAGE HERE
    result = Result.objects.filter(student=studentid,studentclass=classroom,term=activeTerm,session=activeSession).update(termaverage=class_av)
    
    
    # return av


#  subject positioning
def subjectPosition(subject, classroom):
    
    
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')
    
    scores = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession)
    ordered_scores = []
    counter = 1
    repeated_counter = 0
    # index_counter = 0
    previous_score = Scores.objects.none()
    for score in scores.order_by("-subjecttotal"):
        # repeated_counter = 0
        if counter == 1:
            # this is the first iteration, just assign the first position
            position = counter
             # update the database 
            score_entity = Scores.objects.get(pk=score.pk)
            score_entity.subjectposition = position
            score_entity.save()
            # ordered_scores.append({
            # "position": position, 
            # "id": score.pk,
            # "subjecttotal": score.subjecttotal
            # })
            previous_score = score
            counter += 1   
            
            
        else:
            
            # check for duplicate
            if score.subjecttotal == previous_score.subjecttotal:
                # update database
                score_entity = Scores.objects.get(pk=score.pk)
                score_entity.subjectposition = position
                score_entity.save()
                
                # position = counter
                # ordered_scores.append({
                # "position": position, 
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })
                # position = previous_score.position
                repeated_counter +=1
                
            else:
                position = counter + repeated_counter
                # update database
                score_entity = Scores.objects.get(pk=score.pk)
                score_entity.subjectposition = position
                score_entity.save()
                
                # ordered_scores.append({
                # "position": position, 
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })
                
                previous_score = score
                # previous_position = position
                # repeated_counter = position
                
                counter += 1
    # return render(request, "template.html", {"players": ordered_players})
    # return ordered_scores


# assign terminal result position
def terminalPosition(classroom):
    
    
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')
    
    results = Result.objects.filter(studentclass=classroom,term=activeTerm,session=activeSession)
    ordered_scores = []
    counter = 1
    repeated_counter = 0
    
    previous_score = Result.objects.none()
    for result in results.order_by("-termtotal"):
        # repeated_counter = 0
        if counter == 1:
            # this is the first iteration, just assign the first position
            position = counter
             # update the database 
            result_entity = Result.objects.get(pk=result.pk)
            result_entity.termposition = position
            result_entity.save()
            
          
            # ordered_scores.append({
            # "position": position, 
            # "id": score.pk,
            # "subjecttotal": score.subjecttotal
            # })
            previous_score = result
            counter += 1   
        else:
            
            # check for duplicate
            if result.termtotal == previous_score.termtotal:
                # update database
                result_entity = Result.objects.get(pk=result.pk)
                result_entity.termposition = position
                result_entity.save()
                
                # position = counter
                # ordered_scores.append({
                # "position": position, 
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })
                # position = previous_score.position
                repeated_counter +=1
                
            else:
                position = counter + repeated_counter
                # update database
                result_entity = Result.objects.get(pk=result.pk)
                result_entity.termposition = position
                result_entity.save()
                
                # ordered_scores.append({
                # "position": position, 
                # "id": score.pk,
                # "subjecttotal": score.subjecttotal
                # })
                
                previous_score = result
                # previous_position = position
                # repeated_counter = position
                counter += 1
    
# update ratings
def scoresRating(subject,classroom):
    
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')
    
    minMax = minMaxScores(subject,classroom)
    
    scores = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession)
    
    for scoresObj in scores:
        
        if scoresObj.subjecttotal <= 39:
            scoresObj.subjectgrade = 'E'
            scoresObj.subjectrating = 'Poor'
            # scoresObj.highest_inclass = minMax['max_scores']
            # scoresObj.lowest_inclass = minMax['min_scores']
            scoresObj.save()
        elif scoresObj.subjecttotal >= 40 and scoresObj.subjecttotal <= 54.9:
            scoresObj.subjectgrade = 'D'
            scoresObj.subjectrating = 'Fair'
            scoresObj.save()
        elif scoresObj.subjecttotal >= 39 and scoresObj.subjecttotal <= 64.9:
            scoresObj.subjectgrade = 'C'
            scoresObj.subjectrating = 'Good'
            scoresObj.save()
        elif scoresObj.subjecttotal >= 65 and scoresObj.subjecttotal <= 74.9:
            scoresObj.subjectgrade = 'B'
            scoresObj.subjectrating = 'Very Good'
            scoresObj.save()
        elif scoresObj.subjecttotal >= 75 and scoresObj.subjecttotal <= 100:
            
            scoresObj.subjectgrade = 'A'
            scoresObj.subjectrating = 'Excellent'
            scoresObj.save()
        else:
            scoresObj.subjectgrade = 'NA'
            scoresObj.subjectrating = 'NA'
            scoresObj.save()
        

# Minimum and Maximum scores
def minMaxScores(subject,classroom):
    
    # min_max = []
    
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')

    # get scores based on subject
    # scores = Scores.objects.filter(subject=subj,studentclass=classroom,term=activeTerm,session=activeSession).distinct('student').aggregate(Sum('subjAverage'))
    
    min_max = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession).aggregate(min_scores=Min('subjecttotal'),max_scores=Max('subjecttotal'))
    
    scores = Scores.objects.filter(subject=subject,studentclass=classroom,term=activeTerm,session=activeSession).update(highest_inclass=min_max['max_scores'],lowest_inclass=min_max['min_scores'])
    
    
    
    # return min_max


# update subject average
def processScores(subjectObj,classroomObj):
    
    # get active term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')
    
    subjavg = subjectAverage(subjectObj,classroomObj)
    
    scores = Scores.objects.filter(subject=subjectObj,studentclass=classroomObj,term=activeTerm,session=activeSession).update(subjaverage=subjavg)
    
     # update position and grading 
    subjectPosition(subjectObj,classroomObj)
        
    # Update  grades
    scoresRating(subjectObj,classroomObj)
    
    # update min and max
    minMaxScores(subjectObj,classroomObj)
    
    

# Process terminal result
def processTerminalResult(scoresObj):
    

    # Find record in the result table
    result = Result.objects.filter(student=scoresObj.student, studentclass=scoresObj.studentclass, term=scoresObj.term,session=scoresObj.session)
    
    scores = Scores.objects.filter(student=scoresObj.student,studentclass=scoresObj.studentclass,term=scoresObj.term,session=scoresObj.session).aggregate(subject_total=Sum('subjecttotal'))
    
    # print(scores['subject_total'])
    
    # check for existence of record
    if result:
        # update the record
        result.update(termtotal=scores['subject_total'])
        
        # update terminal average
        terminalAverage(scoresObj.student,scoresObj.studentclass)
        # update  term position
        terminalPosition(scoresObj.studentclass)
    else:
        # get class teacher
        # TODO: Add class teacher when creating comments
        class_teacher = ClassTeacher.objects.filter(classroom=scoresObj.studentclass,term=scoresObj.term,session=scoresObj.session)
        for i in class_teacher:
            teacher = i.teacher

        # create a new record
        resultObj = Result.objects.create(
                                 termtotal = scores['subject_total'],
                                 classteacher = ClassTeacher.objects.get(pk=teacher.id),
                                 session = scoresObj.session,
                                 studentclass = scoresObj.studentclass,
                                 term = scoresObj.term,
                                 client = scoresObj.client,
                                 student = scoresObj.student
                                     )
        new_Result = resultObj.save()

        # update term average
        terminalAverage(scoresObj.student,scoresObj.studentclass)
        
        # update  term position
        terminalPosition(scoresObj.studentclass)
        
# delete result object
def deleteResult(studentid,classroom):
    
     # get sctive term and session
    activeTerm = Term.objects.get(status='True')
    activeSession = Session.objects.get(status='True')
    
    result = Result.objects.filter(student=studentid,studentclass=classroom,term=activeTerm,session=activeSession).first()
    
    if result:
        result.delete()