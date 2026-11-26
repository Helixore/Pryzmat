// Router-registered endpoints keep the trailing slash (DefaultRouter).
// login and dashboard are plain path() entries without one.
export const ENDPOINTS = {
  login: '/api/v1/login',
  dashboard: '/api/v1/dashboard',
  studentClass: '/api/v1/studentclass/',
  teacher: '/api/v1/teacher/',
  student: '/api/v1/student/',
  parent: '/api/v1/parent/',
  grade: '/api/v1/grade/',
  lesson: '/api/v1/lesson/',
  presence: '/api/v1/presence/',
  message: '/api/v1/message/',
  schedule: '/api/v1/schedule/',
  subject: '/api/v1/subject/',
  substitution: '/api/v1/substitution/',
  conductEntry: '/api/v1/conductentries/',
  principal: '/api/v1/principal/',
  worker: '/api/v1/worker/',
};
