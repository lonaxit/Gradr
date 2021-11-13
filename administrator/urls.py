from django.urls import path
from . import views


urlpatterns = [
  path('setting', views.createClient, name='admin-setting'),
  path('update-profile/<str:pk>', views.updateClient, name='update-profile'),
  path('add-term', views.addTerm, name='create-term'),
  path('update-term/<str:pk>', views.editTerm, name='update-term'),
  path('profile', views.profile, name='admin-profile'),
  path('session', views.addSession, name='add-session'),
  path('all-sessions', views.allSessions, name='all-sessions'),
  path('update-session/<str:pk>', views.updateSession, name='update-session'),
  path('class', views.addClass, name='add-class'),
  path('update-class/<str:pk>', views.updateClass, name='update-class'),
  path('all-classes', views.allClasses, name='all-classes'),
  path('subject', views.addSubject, name='add-subject'),
  path('update-subject/<str:pk>', views.updateSubject, name='update-subject'),
  path('all-subjects', views.allSubjects, name='all-subjects'),
  path('attendance-setting', views.attendance_settings, name='attendance-setting'),
  path('resumption-setting', views.resumption_settings, name='resumption-setting'),
  path('resumption-dates', views.resumptionDates, name='resumption-dates'),
  path('update-resumption/<str:pk>', views.updateResumption, name='update-resumption'),
  path('subject-perclass', views.subjectPerClass, name='subject-perclass'),
  path('subject-perclass-list', views.listSubjectPerClass, name='subject-perclass-list'),
  path('subject-perclass-list/<str:pk>', views.updateSubjectPerClass, name='update-subject-perclass-list'),
  path('new-student', views.newStudent, name='new-student'),
  path('update-student/<str:pk>', views.updateStudentProfile, name='update-student'),
  path('view-student/<str:pk>', views.viewStudent, name='view-student'),
  path('student-photo/<str:pk>', views.studentPhoto, name='student-photo'),
  path('list-students', views.listStudents, name='list-students'),
  path('update-number/<str:pk>', views.updateNumber, name='update-number'),
  path('define-prefix', views.definePrefix, name='define-prefix'),
  path('list-prefix', views.listPrefix, name='list-prefix'),
  path('update-prefix/<str:pk>', views.updatePrefix, name='update-prefix'),


  # path('country-json', views.get_json_country_data, name='country-json'),
  path('state-json/<str:pk>', views.get_json_state_data, name='state-json'),
  path('lg-json/<str:pk>', views.get_json_lg_data, name='lg-json'),

  path('new-teacher', views.newTeacher, name='new-teacher'),
  path('update-teacher/<str:pk>', views.updateTeacherProfile, name='update-teacher'),
  path('view-teacher/<str:pk>', views.viewTeacher, name='view-teacher'),
  path('list-teacher', views.listTeacher, name='list-teacher'),
  path('block-teacher/<str:pk>', views.blockTeacher, name='block-teacher'),
  path('teacher-photo/<str:pk>', views.teacherPhoto, name='teacher-photo'),
  path('assign-subject', views.assignSubject, name='assign-subject'),
  path('update-subject-teacher/<str:pk>', views.updateSubjectTeacher, name='update-subject-teacher'),

  path('list-subject-teachers', views.listSubjectTeachers, name='list-subject-teachers'),
  path('assign-class-teacher', views.assignClassTeacher, name='assign-class-teacher'),
  path('list-class-teacher', views.listClassTeacher, name='list-class-teacher'),
  path('update-class-teacher/<str:pk>', views.updateClassTeacher, name='update-class-teacher'),
  path('admission-list', views.admissionList, name='admission-list'),
  path('export-admission-list/<str:session>/<str:classroom>/<str:term>', views.exportAdmissionList, name='export-admission'),

  path('add-affective', views.addAffective, name='add-affective'),
  path('list-affective', views.listAffective, name='list-affective'),
  path('update-affective/<str:pk>', views.updateAffective, name='update-affective'),

  path('add-psychomotor', views.addPsychomotor, name='add-psychomotor'),
  path('list-psychomotor', views.listPsychomotor, name='list-psychomotor'),
  path('update-psychomotor/<str:pk>', views.updatePsychomotor, name='update-psychomotor'),

  path('add-rating', views.addRating, name='add-rating'),
  path('list-rating', views.listRating, name='list-rating'),
  path('update-rating/<str:pk>', views.updateRating, name='update-rating'),
  path('generate-numbers', views.generateAdmissionNumber, name='generate-numbers'),

  # filter scores
  path('scores-summary', views.scoresFilter, name='scores-summary'),
  path('comment-result', views.resultFilter, name='comment-result'),
  path('result-analysis', views.resultAnalysis, name='result-analysis'),
  path('approve-result/<str:classroom>/<str:term>/<str:session>', views.approveResult, name='approve-result'),
  
  # institution
   path('logo/<str:pk>', views.logo, name='logo'),
   
  #for migration purposes
  path('process-my-result', views.processMyResult, name='process-my-result'),
  path('bulk-create-student', views.importBulkAssessment, name='create-students'),
  path('bulk-exams', views.importBulkExams, name='bulk-exams'),
  
  

]
